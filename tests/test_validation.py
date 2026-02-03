"""
Tests for Marshmallow Validation
"""
import pytest
from marshmallow import ValidationError
from app.schemas import (
    UserSchema, UserUpdateSchema, PostSchema, PostUpdateSchema,
    LoginSchema, RegisterSchema, PaginationSchema
)


class TestUserValidation:
    """Test user validation schemas"""

    def test_valid_user_schema(self):
        """Test valid user data"""
        schema = UserSchema()
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        result = schema.load(data)
        assert result['username'] == 'testuser'
        assert result['email'] == 'test@example.com'

    def test_missing_required_fields(self):
        """Test missing required fields"""
        schema = UserSchema()
        data = {'username': 'testuser'}
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        errors = exc_info.value.messages
        assert 'email' in errors
        assert 'password' in errors

    def test_invalid_email(self):
        """Test invalid email format"""
        schema = UserSchema()
        data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password': 'password123'
        }
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        errors = exc_info.value.messages
        assert 'email' in errors

    def test_short_password(self):
        """Test password too short"""
        schema = UserSchema()
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': '12345'
        }
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        errors = exc_info.value.messages
        assert 'password' in errors

    def test_username_too_short(self):
        """Test username too short"""
        schema = UserSchema()
        data = {
            'username': 'ab',
            'email': 'test@example.com',
            'password': 'password123'
        }
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        errors = exc_info.value.messages
        assert 'username' in errors

    def test_user_update_schema_all_optional(self):
        """Test user update schema allows partial data"""
        schema = UserUpdateSchema()
        data = {'first_name': 'Updated'}
        result = schema.load(data)
        assert result['first_name'] == 'Updated'


class TestPostValidation:
    """Test post validation schemas"""

    def test_valid_post_schema(self):
        """Test valid post data"""
        schema = PostSchema()
        data = {
            'title': 'Test Post',
            'content': 'This is test content',
            'summary': 'Test summary',
            'published': True
        }
        result = schema.load(data)
        assert result['title'] == 'Test Post'
        assert result['published'] == True

    def test_missing_required_post_fields(self):
        """Test missing required post fields"""
        schema = PostSchema()
        data = {'title': 'Test Post'}
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        errors = exc_info.value.messages
        assert 'content' in errors

    def test_post_title_too_long(self):
        """Test post title exceeds max length"""
        schema = PostSchema()
        data = {
            'title': 'x' * 201,
            'content': 'Test content'
        }
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        errors = exc_info.value.messages
        assert 'title' in errors

    def test_post_summary_too_long(self):
        """Test post summary exceeds max length"""
        schema = PostSchema()
        data = {
            'title': 'Test Post',
            'content': 'Test content',
            'summary': 'x' * 501
        }
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        errors = exc_info.value.messages
        assert 'summary' in errors

    def test_post_update_allows_partial(self):
        """Test post update allows partial data"""
        schema = PostUpdateSchema()
        data = {'title': 'Updated Title'}
        result = schema.load(data)
        assert result['title'] == 'Updated Title'


class TestAuthValidation:
    """Test authentication validation schemas"""

    def test_valid_login(self):
        """Test valid login data"""
        schema = LoginSchema()
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        result = schema.load(data)
        assert result['username'] == 'testuser'

    def test_missing_login_fields(self):
        """Test missing login fields"""
        schema = LoginSchema()
        data = {'username': 'testuser'}
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        errors = exc_info.value.messages
        assert 'password' in errors


class TestPaginationValidation:
    """Test pagination validation schemas"""

    def test_valid_pagination(self):
        """Test valid pagination parameters"""
        schema = PaginationSchema()
        data = {
            'page': 2,
            'per_page': 25,
            'q': 'search query',
            'sort': 'created_at',
            'order': 'asc'
        }
        result = schema.load(data)
        assert result['page'] == 2
        assert result['per_page'] == 25
        assert result['order'] == 'asc'

    def test_default_values(self):
        """Test default pagination values"""
        schema = PaginationSchema()
        result = schema.load({})
        assert result['page'] == 1
        assert result['per_page'] == 20
        assert result['sort'] == 'created_at'
        assert result['order'] == 'desc'

    def test_invalid_page_number(self):
        """Test invalid page number"""
        schema = PaginationSchema()
        data = {'page': 0}
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        errors = exc_info.value.messages
        assert 'page' in errors

    def test_invalid_per_page(self):
        """Test invalid per_page value"""
        schema = PaginationSchema()
        data = {'per_page': 0}
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        errors = exc_info.value.messages
        assert 'per_page' in errors

    def test_per_page_exceeds_max(self):
        """Test per_page exceeds maximum"""
        schema = PaginationSchema()
        data = {'per_page': 150}
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        errors = exc_info.value.messages
        assert 'per_page' in errors

    def test_invalid_order_value(self):
        """Test invalid sort order"""
        schema = PaginationSchema()
        data = {'order': 'invalid'}
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        errors = exc_info.value.messages
        assert 'order' in errors
