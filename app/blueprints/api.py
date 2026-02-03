"""
API Blueprint - RESTful API Endpoints
"""
from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db
from app.models.user import User, Post

api_bp = Blueprint('api', __name__)
api = Api(api_bp,
          version='1.0',
          title='Flask Starter API',
          description='Professional Flask API with React frontend',
          doc='/docs',
          prefix='/api/v1')

# API Models
user_model = api.model('User', {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'is_admin': fields.Boolean,
    'created_at': fields.DateTime
})

post_model = api.model('Post', {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'summary': fields.String,
    'published': fields.Boolean,
    'user_id': fields.Integer,
    'created_at': fields.DateTime
})

# Namespaces
users_ns = api.namespace('users', description='User operations')
posts_ns = api.namespace('posts', description='Post operations')


@users_ns.route('/')
class UserList(Resource):
    """User list and creation"""

    def get(self):
        """List all users with pagination"""
        from app.utils.pagination import paginate_query
        query = User.query
        return paginate_query(query)

    @api.expect(user_model)
    def post(self):
        """Create new user"""
        data = request.get_json()
        
        if not data.get('username') or not data.get('email') or not data.get('password'):
            return {'error': 'Missing required fields'}, 400
        
        if User.query.filter_by(username=data['username']).first():
            return {'error': 'Username already exists'}, 400
        
        if User.query.filter_by(email=data['email']).first():
            return {'error': 'Email already exists'}, 400
        
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
class UserDetail(Resource):
    """User details"""
    
    def get(self, user_id):
        """Get user by ID"""
        user = User.query.get_or_404(user_id)
        return user.to_dict()

    @jwt_required()
    @api.expect(user_model)
    def put(self, user_id):
        """Update user"""
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        if current_user_id != user_id and not user.is_admin:
            return {'error': 'Unauthorized'}, 403
        
        data = request.get_json()
        
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        
        user.save()
        return user.to_dict()

    @jwt_required()
    def delete(self, user_id):
        """Delete user"""
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        if current_user_id != user_id and not user.is_admin:
            return {'error': 'Unauthorized'}, 403
        
        user.delete()
        return '', 204


@posts_ns.route('/')
class PostList(Resource):
    """Post list and creation"""

    def get(self):
        """List all published posts with pagination"""
        from app.utils.pagination import paginate_query
        query = Post.query.filter_by(published=True)
        return paginate_query(query)

    @jwt_required()
    @api.expect(post_model)
    def post(self):
        """Create new post"""
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('title') or not data.get('content'):
            return {'error': 'Title and content required'}, 400
        
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
class PostDetail(Resource):
    """Post details"""
    
    def get(self, post_id):
        """Get post by ID"""
        post = Post.query.get_or_404(post_id)
        return post.to_dict()

    @jwt_required()
    @api.expect(post_model)
    def put(self, post_id):
        """Update post"""
        current_user_id = get_jwt_identity()
        post = Post.query.get_or_404(post_id)
        
        if post.user_id != current_user_id:
            return {'error': 'Unauthorized'}, 403
        
        data = request.get_json()
        
        if 'title' in data:
            post.title = data['title']
        if 'content' in data:
            post.content = data['content']
        if 'summary' in data:
            post.summary = data['summary']
        if 'published' in data:
            post.published = data['published']
        
        post.save()
        return post.to_dict()

    @jwt_required()
    def delete(self, post_id):
        """Delete post"""
        current_user_id = get_jwt_identity()
        post = Post.query.get_or_404(post_id)
        
        if post.user_id != current_user_id:
            return {'error': 'Unauthorized'}, 403
        
        post.delete()
        return '', 204
