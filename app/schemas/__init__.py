"""
Request/Response Validation Schemas
"""
from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models import db
from app.models.user import User


class BaseSchema(Schema):
    """Base schema with common fields"""
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class UserSchema(BaseSchema):
    """User schema for validation"""
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=80),
        metadata={"description": "Unique username"}
    )
    email = fields.Email(
        required=True,
        validate=validate.Length(max=120),
        metadata={"description": "User email address"}
    )
    password = fields.Str(
        load_only=True,
        validate=validate.Length(min=6, max=128),
        metadata={"description": "User password (write-only)"}
    )
    first_name = fields.Str(
        validate=validate.Length(max=50),
        metadata={"description": "User first name"}
    )
    last_name = fields.Str(
        validate=validate.Length(max=50),
        metadata={"description": "User last name"}
    )
    is_admin = fields.Bool(
        dump_only=True,
        metadata={"description": "Admin status flag"}
    )
    is_active = fields.Bool(
        dump_only=True,
        metadata={"description": "Active status flag"}
    )
    last_login = fields.DateTime(
        dump_only=True,
        metadata={"description": "Last login timestamp"}
    )

    @validates('username')
    def validate_username(self, value):
        """Validate username is unique"""
        user = User.query.filter_by(username=value).first()
        if user:
            raise ValidationError('Username already exists')

    @validates('email')
    def validate_email(self, value):
        """Validate email is unique"""
        user = User.query.filter_by(email=value).first()
        if user:
            raise ValidationError('Email already exists')


class UserUpdateSchema(Schema):
    """User update schema (all fields optional)"""
    username = fields.Str(
        validate=validate.Length(min=3, max=80)
    )
    email = fields.Email(
        validate=validate.Length(max=120)
    )
    first_name = fields.Str(
        validate=validate.Length(max=50)
    )
    last_name = fields.Str(
        validate=validate.Length(max=50)
    )


class PostSchema(BaseSchema):
    """Post schema for validation"""
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200),
        metadata={"description": "Post title"}
    )
    content = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        metadata={"description": "Post content"}
    )
    summary = fields.Str(
        validate=validate.Length(max=500),
        metadata={"description": "Post summary"}
    )
    published = fields.Bool(
        missing=False,
        metadata={"description": "Published status flag"}
    )
    user_id = fields.Int(
        dump_only=True,
        metadata={"description": "Author user ID"}
    )


class PostUpdateSchema(Schema):
    """Post update schema (all fields optional)"""
    title = fields.Str(
        validate=validate.Length(min=1, max=200)
    )
    content = fields.Str(
        validate=validate.Length(min=1)
    )
    summary = fields.Str(
        validate=validate.Length(max=500)
    )
    published = fields.Bool()


class LoginSchema(Schema):
    """Login request schema"""
    username = fields.Str(
        required=True,
        metadata={"description": "Username or email"}
    )
    password = fields.Str(
        required=True,
        load_only=True,
        metadata={"description": "User password"}
    )


class RegisterSchema(UserSchema):
    """Registration schema - extends UserSchema"""
    pass


class PaginationSchema(Schema):
    """Pagination parameters schema"""
    page = fields.Int(
        missing=1,
        validate=validate.Range(min=1),
        metadata={"description": "Page number"}
    )
    per_page = fields.Int(
        missing=20,
        validate=validate.Range(min=1, max=100),
        metadata={"description": "Items per page"}
    )
    q = fields.Str(
        metadata={"description": "Search query"}
    )
    sort = fields.Str(
        missing='created_at',
        metadata={"description": "Sort field"}
    )
    order = fields.Str(
        missing='desc',
        validate=validate.OneOf(['asc', 'desc']),
        metadata={"description": "Sort order (asc or desc)"}
    )


class ApiResponseSchema(Schema):
    """API response wrapper schema"""
    success = fields.Bool(
        metadata={"description": "Request success status"}
    )
    data = fields.Dict(
        metadata={"description": "Response data"}
    )
    error = fields.Str(
        metadata={"description": "Error message if failed"}
    )
    meta = fields.Dict(
        metadata={"description": "Pagination metadata"}
    )
