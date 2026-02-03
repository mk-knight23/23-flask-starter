"""
API V2 Blueprint - Enhanced RESTful API with pagination and validation
"""
from flask import Blueprint, request
from flask_restx import Api, Resource, fields, namespace
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db
from app.models.user import User, Post
from app.utils.pagination import (
    paginate_query,
    build_search_params,
    apply_filters,
    apply_search,
    apply_sorting
)
from app.schemas import (
    UserSchema, UserUpdateSchema, PostSchema, PostUpdateSchema,
    LoginSchema, PaginationSchema
)
from marshmallow import ValidationError

api_v2_bp = Blueprint('api_v2', __name__)
api = Api(api_v2_bp,
          version='2.0',
          title='Flask Starter API V2',
          description='Enhanced API with pagination and validation',
          doc='/docs',
          prefix='/api/v2')

# Namespaces
users_ns = api.namespace('users', description='User operations V2')
posts_ns = api.namespace('posts', description='Post operations V2')
auth_ns = api.namespace('auth', description='Authentication V2')

# API Models for Swagger
user_model_v2 = api.model('UserV2', {
    'id': fields.Integer(description='User ID'),
    'username': fields.String(description='Username'),
    'email': fields.String(description='Email address'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'is_admin': fields.Boolean(description='Admin status'),
    'is_active': fields.Boolean(description='Active status'),
    'last_login': fields.DateTime(description='Last login timestamp'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

post_model_v2 = api.model('PostV2', {
    'id': fields.Integer(description='Post ID'),
    'title': fields.String(description='Post title'),
    'content': fields.String(description='Post content'),
    'summary': fields.String(description='Post summary'),
    'published': fields.Boolean(description='Published status'),
    'user_id': fields.Integer(description='Author user ID'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

pagination_model = api.model('Pagination', {
    'page': fields.Integer(description='Current page'),
    'per_page': fields.Integer(description='Items per page'),
    'total': fields.Integer(description='Total items'),
    'total_pages': fields.Integer(description='Total pages'),
    'has_next': fields.Boolean(description='Has next page'),
    'has_prev': fields.Boolean(description='Has previous page'),
    'next_page': fields.Integer(description='Next page number'),
    'prev_page': fields.Integer(description='Previous page number')
})

user_list_model_v2 = api.model('UserListV2', {
    'data': fields.List(fields.Nested(user_model_v2), description='List of users'),
    'meta': fields.Nested(pagination_model, description='Pagination metadata')
})

post_list_model_v2 = api.model('PostListV2', {
    'data': fields.List(fields.Nested(post_model_v2), description='List of posts'),
    'meta': fields.Nested(pagination_model, description='Pagination metadata')
})


@users_ns.route('/')
class UserListV2(Resource):
    """User list and creation with pagination"""

    @api.doc('list_users_v2')
    @api.response(200, 'Success', user_list_model_v2)
    @api.param('page', 'Page number', type='integer', default=1)
    @api.param('per_page', 'Items per page', type='integer', default=20)
    @api.param('q', 'Search query')
    @api.param('sort', 'Sort field', default='created_at')
    @api.param('order', 'Sort order (asc/desc)', default='desc')
    def get(self):
        """
        List all users with pagination and search

        Supports:
        - Pagination (page, per_page)
        - Full-text search (q)
        - Sorting (sort, order)
        - Filtering by any field
        """
        query = User.query

        # Apply search, filters, and sorting
        filters, search_query, sort_field, sort_dir = build_search_params(
            User,
            search_fields=['username', 'email', 'first_name', 'last_name']
        )

        query = apply_search(query, User, search_query, ['username', 'email', 'first_name', 'last_name'])
        query = apply_filters(query, User, filters)
        query = apply_sorting(query, User, sort_field, sort_dir)

        # Paginate
        result = paginate_query(query, serializer=lambda u: {
            **u.to_dict(),
            'post_count': u.posts.count()
        })

        return result

    @api.doc('create_user_v2')
    @api.expect(user_model_v2)
    @api.response(201, 'User created', user_model_v2)
    @api.response(400, 'Validation error')
    def post(self):
        """
        Create new user with validation

        Validates:
        - Username uniqueness
        - Email uniqueness
        - Password strength
        - Field lengths
        """
        schema = UserSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {'error': 'Validation failed', 'messages': err.messages}, 400

        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        user.set_password(data['password'])
        user.save()

        return user.to_dict(), 201


@users_ns.route('/<int:user_id>')
@users_ns.response(404, 'User not found')
@users_ns.response(400, 'Invalid user ID')
class UserDetailV2(Resource):
    """User details, update, and delete"""

    @api.doc('get_user_v2')
    @api.response(200, 'Success', user_model_v2)
    def get(self, user_id):
        """Get user by ID with post count"""
        user = User.query.get_or_404(user_id)
        data = user.to_dict()
        data['post_count'] = user.posts.count()
        return data

    @jwt_required()
    @api.doc('update_user_v2')
    @api.expect(user_model_v2)
    @api.response(200, 'User updated', user_model_v2)
    @api.response(403, 'Forbidden')
    @api.response(400, 'Validation error')
    def put(self, user_id):
        """
        Update user with validation

        Requires JWT token. Users can only update their own profile
        unless they are admins.
        """
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        current_user = User.query.get(current_user_id)

        if current_user_id != user_id and not current_user.is_admin:
            return {'error': 'Unauthorized - can only update own profile'}, 403

        schema = UserUpdateSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {'error': 'Validation failed', 'messages': err.messages}, 400

        # Update fields
        for field in ['username', 'email', 'first_name', 'last_name']:
            if field in data:
                # Check uniqueness for username/email
                if field in ['username', 'email']:
                    existing = User.query.filter(
                        getattr(User, field) == data[field],
                        User.id != user_id
                    ).first()
                    if existing:
                        return {'error': f'{field} already exists'}, 400
                setattr(user, field, data[field])

        user.save()
        return user.to_dict()

    @jwt_required()
    @api.doc('delete_user_v2')
    @api.response(204, 'User deleted')
    @api.response(403, 'Forbidden')
    def delete(self, user_id):
        """
        Delete user

        Requires JWT token. Users can only delete themselves
        unless they are admins.
        """
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        current_user = User.query.get(current_user_id)

        if current_user_id != user_id and not current_user.is_admin:
            return {'error': 'Unauthorized - can only delete own profile'}, 403

        user.delete()
        return '', 204


@posts_ns.route('/')
class PostListV2(Resource):
    """Post list and creation with pagination"""

    @api.doc('list_posts_v2')
    @api.response(200, 'Success', post_list_model_v2)
    @api.param('page', 'Page number', type='integer', default=1)
    @api.param('per_page', 'Items per page', type='integer', default=20)
    @api.param('q', 'Search query')
    @api.param('sort', 'Sort field', default='created_at')
    @api.param('order', 'Sort order (asc/desc)', default='desc')
    @api.param('published', 'Filter by published status')
    def get(self):
        """
        List all posts with pagination and search

        Supports:
        - Pagination (page, per_page)
        - Full-text search (q)
        - Sorting (sort, order)
        - Filtering by published status
        """
        query = Post.query

        # Build search parameters
        filters, search_query, sort_field, sort_dir = build_search_params(
            Post,
            search_fields=['title', 'content', 'summary']
        )

        # Apply search, filters, and sorting
        query = apply_search(query, Post, search_query, ['title', 'content', 'summary'])
        query = apply_filters(query, Post, filters)
        query = apply_sorting(query, Post, sort_field, sort_dir)

        # Paginate with author info
        result = paginate_query(query, serializer=lambda p: {
            **p.to_dict(),
            'author_username': p.author.username if p.author else None
        })

        return result

    @jwt_required()
    @api.doc('create_post_v2')
    @api.expect(post_model_v2)
    @api.response(201, 'Post created', post_model_v2)
    @api.response(400, 'Validation error')
    def post(self):
        """
        Create new post with validation

        Requires JWT token. Automatically sets author to current user.
        """
        current_user_id = get_jwt_identity()

        schema = PostSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {'error': 'Validation failed', 'messages': err.messages}, 400

        post = Post(
            title=data['title'],
            content=data['content'],
            summary=data.get('summary', ''),
            published=data.get('published', False),
            user_id=current_user_id
        )
        post.save()

        return post.to_dict(), 201


@posts_ns.route('/<int:post_id>')
@posts_ns.response(404, 'Post not found')
class PostDetailV2(Resource):
    """Post details, update, and delete"""

    @api.doc('get_post_v2')
    @api.response(200, 'Success', post_model_v2)
    def get(self, post_id):
        """Get post by ID with author info"""
        post = Post.query.get_or_404(post_id)
        data = post.to_dict()
        data['author_username'] = post.author.username if post.author else None
        return data

    @jwt_required()
    @api.doc('update_post_v2')
    @api.expect(post_model_v2)
    @api.response(200, 'Post updated', post_model_v2)
    @api.response(403, 'Forbidden')
    @api.response(400, 'Validation error')
    def put(self, post_id):
        """
        Update post with validation

        Requires JWT token. Only the author can update their posts.
        """
        current_user_id = get_jwt_identity()
        post = Post.query.get_or_404(post_id)

        if post.user_id != current_user_id:
            return {'error': 'Unauthorized - can only update own posts'}, 403

        schema = PostUpdateSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {'error': 'Validation failed', 'messages': err.messages}, 400

        # Update fields
        for field in ['title', 'content', 'summary', 'published']:
            if field in data:
                setattr(post, field, data[field])

        post.save()
        return post.to_dict()

    @jwt_required()
    @api.doc('delete_post_v2')
    @api.response(204, 'Post deleted')
    @api.response(403, 'Forbidden')
    def delete(self, post_id):
        """
        Delete post

        Requires JWT token. Only the author can delete their posts.
        """
        current_user_id = get_jwt_identity()
        post = Post.query.get_or_404(post_id)

        if post.user_id != current_user_id:
            return {'error': 'Unauthorized - can only delete own posts'}, 403

        post.delete()
        return '', 204


@auth_ns.route('/login')
class AuthLoginV2(Resource):
    """Authentication endpoint"""

    @api.doc('login_v2')
    @api.expect(api.model('Login', {
        'username': fields.String(required=True, description='Username or email'),
        'password': fields.String(required=True, description='Password')
    }))
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """
        Authenticate user and return JWT token

        Accepts username or email and password.
        Returns JWT access token on success.
        """
        schema = LoginSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return {'error': 'Validation failed', 'messages': err.messages}, 400

        # Try username first, then email
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            user = User.query.filter_by(email=data['username']).first()

        if not user or not user.check_password(data['password']):
            return {'error': 'Invalid credentials'}, 401

        if not user.is_active:
            return {'error': 'Account is inactive'}, 401

        from flask_jwt_extended import create_access_token
        access_token = create_access_token(identity=user.id)

        return {
            'access_token': access_token,
            'user': user.to_dict()
        }, 200
