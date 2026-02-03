"""
Tests for Admin Panel
"""
import pytest
from app.models import db
from app.models.user import User, Post


class TestAdminPanel:
    """Test admin panel functionality"""

    def test_admin_accessible(self, client):
        """Test admin panel is accessible"""
        response = client.get('/admin/')
        assert response.status_code in [200, 302, 401]  # May redirect or require auth

    def test_admin_user_view(self, client):
        """Test admin user model view"""
        user = User(username='admin', email='admin@example.com', is_admin=True)
        user.set_password('admin123')
        user.save()

        # Admin views should be accessible
        response = client.get('/admin/user/')
        assert response.status_code in [200, 302, 401]

    def test_admin_post_view(self, client):
        """Test admin post model view"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        user.save()

        post = Post(
            title='Test Post',
            content='Test content',
            published=True,
            user_id=user.id
        )
        post.save()

        # Admin post view should be accessible
        response = client.get('/admin/post/')
        assert response.status_code in [200, 302, 401]

    def test_admin_create_user(self, client):
        """Test creating user through admin"""
        # This test verifies the admin interface can be used
        # Actual creation would require authentication and form submission
        admin_url = '/admin/user/new/'
        response = client.get(admin_url)
        assert response.status_code in [200, 302, 401]

    def test_admin_edit_user(self, client):
        """Test editing user through admin"""
        user = User(username='edituser', email='edit@example.com')
        user.set_password('password123')
        user.save()

        edit_url = f'/admin/user/edit/?id={user.id}'
        response = client.get(edit_url)
        assert response.status_code in [200, 302, 401]

    def test_admin_delete_user(self, client):
        """Test deleting user through admin"""
        user = User(username='deleteuser', email='delete@example.com')
        user.set_password('password123')
        user.save()

        delete_url = f'/admin/user/delete/?id={user.id}'
        response = client.get(delete_url)
        assert response.status_code in [200, 302, 401]
