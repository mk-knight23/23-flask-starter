"""
Tests for API V2 endpoints
"""
import pytest
from flask import json
from app.models import db
from app.models.user import User, Post


class TestUsersV2:
    """Test user endpoints V2"""

    def test_list_users_pagination(self, client):
        """Test user list with pagination"""
        # Create test users
        for i in range(25):
            user = User(
                username=f'testuser{i}',
                email=f'test{i}@example.com'
            )
            user.set_password('password123')
            user.save()

        response = client.get('/api/v2/users/?page=1&per_page=10')
        assert response.status_code == 200
        data = response.get_json()
        assert 'data' in data
        assert 'meta' in data
        assert len(data['data']) == 10
        assert data['meta']['total'] == 25
        assert data['meta']['total_pages'] == 3

    def test_search_users(self, client):
        """Test user search functionality"""
        user1 = User(username='john_doe', email='john@example.com')
        user1.set_password('password123')
        user1.save()

        user2 = User(username='jane_doe', email='jane@example.com')
        user2.set_password('password123')
        user2.save()

        response = client.get('/api/v2/users/?q=john')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['data']) == 1
        assert data['data'][0]['username'] == 'john_doe'

    def test_create_user_validation(self, client):
        """Test user creation with validation"""
        # Test missing fields
        response = client.post('/api/v2/users/',
                              json={'username': 'test'},
                              content_type='application/json')
        assert response.status_code == 400

        # Test valid creation
        response = client.post('/api/v2/users/',
                              json={
                                  'username': 'testuser',
                                  'email': 'test@example.com',
                                  'password': 'password123',
                                  'first_name': 'Test',
                                  'last_name': 'User'
                              },
                              content_type='application/json')
        assert response.status_code == 201
        data = response.get_json()
        assert data['username'] == 'testuser'
        assert data['email'] == 'test@example.com'
        assert 'password' not in data

    def test_duplicate_username_validation(self, client):
        """Test duplicate username validation"""
        user = User(username='testuser', email='test1@example.com')
        user.set_password('password123')
        user.save()

        response = client.post('/api/v2/users/',
                              json={
                                  'username': 'testuser',
                                  'email': 'test2@example.com',
                                  'password': 'password123'
                              },
                              content_type='application/json')
        assert response.status_code == 400

    def test_update_user_with_auth(self, client, auth_headers):
        """Test user update with authentication"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        user.save()

        response = client.put(f'/api/v2/users/{user.id}',
                             json={'first_name': 'Updated'},
                             headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['first_name'] == 'Updated'


class TestPostsV2:
    """Test post endpoints V2"""

    def test_list_posts_pagination(self, client):
        """Test post list with pagination"""
        # Create test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        user.save()

        # Create test posts
        for i in range(15):
            post = Post(
                title=f'Test Post {i}',
                content=f'Content {i}',
                published=True,
                user_id=user.id
            )
            post.save()

        response = client.get('/api/v2/posts/?page=1&per_page=10')
        assert response.status_code == 200
        data = response.get_json()
        assert 'data' in data
        assert 'meta' in data
        assert len(data['data']) == 10
        assert data['meta']['total'] == 15

    def test_search_posts(self, client):
        """Test post search functionality"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        user.save()

        post1 = Post(
            title='Python Tutorial',
            content='Learn Python programming',
            published=True,
            user_id=user.id
        )
        post1.save()

        post2 = Post(
            title='JavaScript Guide',
            content='Learn JavaScript',
            published=True,
            user_id=user.id
        )
        post2.save()

        response = client.get('/api/v2/posts/?q=Python')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['data']) == 1
        assert 'Python' in data['data'][0]['title']

    def test_create_post_with_auth(self, client, auth_headers):
        """Test post creation with authentication"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        user.save()

        response = client.post('/api/v2/posts/',
                              json={
                                  'title': 'Test Post',
                                  'content': 'Test content',
                                  'summary': 'Test summary',
                                  'published': True
                              },
                              headers=auth_headers)
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'Test Post'
        assert data['user_id'] == user.id

    def test_create_post_validation(self, client, auth_headers):
        """Test post creation with validation"""
        response = client.post('/api/v2/posts/',
                              json={'title': 'Test'},
                              headers=auth_headers)
        assert response.status_code == 400

    def test_update_post_authorization(self, client, auth_headers):
        """Test post update authorization"""
        user1 = User(username='user1', email='user1@example.com')
        user1.set_password('password123')
        user1.save()

        user2 = User(username='user2', email='user2@example.com')
        user2.set_password('password123')
        user2.save()

        post = Post(
            title='Original Title',
            content='Original content',
            published=True,
            user_id=user1.id
        )
        post.save()

        # Try to update with user2 (should fail)
        response = client.put(f'/api/v2/posts/{post.id}',
                             json={'title': 'Updated Title'},
                             headers=auth_headers)
        assert response.status_code == 403


class TestAuthV2:
    """Test authentication V2"""

    def test_login_with_username(self, client):
        """Test login with username"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        user.save()

        response = client.post('/api/v2/auth/login',
                              json={
                                  'username': 'testuser',
                                  'password': 'password123'
                              },
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'user' in data
        assert data['user']['username'] == 'testuser'

    def test_login_with_email(self, client):
        """Test login with email"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        user.save()

        response = client.post('/api/v2/auth/login',
                              json={
                                  'username': 'test@example.com',
                                  'password': 'password123'
                              },
                              content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data

    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post('/api/v2/auth/login',
                              json={
                                  'username': 'nonexistent',
                                  'password': 'wrongpassword'
                              },
                              content_type='application/json')
        assert response.status_code == 401

    def test_login_validation(self, client):
        """Test login validation"""
        response = client.post('/api/v2/auth/login',
                              json={'username': 'test'},
                              content_type='application/json')
        assert response.status_code == 400


class TestPagination:
    """Test pagination utilities"""

    def test_page_bounds(self, client):
        """Test pagination page bounds"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        user.save()

        for i in range(5):
            post = Post(
                title=f'Post {i}',
                content=f'Content {i}',
                published=True,
                user_id=user.id
            )
            post.save()

        # Test page too high
        response = client.get('/api/v2/posts/?page=999')
        assert response.status_code == 200
        data = response.get_json()
        assert data['meta']['page'] == 1  # Should default to page 1

    def test_per_page_limits(self, client):
        """Test per_page limits"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        user.save()

        for i in range(150):
            post = Post(
                title=f'Post {i}',
                content=f'Content {i}',
                published=True,
                user_id=user.id
            )
            post.save()

        # Test per_page too high
        response = client.get('/api/v2/posts/?per_page=200')
        assert response.status_code == 200
        data = response.get_json()
        assert data['meta']['per_page'] == 100  # Should max at 100
