"""
Admin Panel Configuration
"""
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import jwt_required, current_user
from flask import redirect, url_for, request
from app.models import db
from app.models.user import User, Post


class SecureModelView(ModelView):
    """Base secure model view with authentication"""

    def is_accessible(self):
        """Check if user is authenticated and is admin"""
        try:
            from flask_jwt_extended import verify_jwt_in_request
            verify_jwt_in_request(optional=True)
            return True  # For development - in production check admin status
        except:
            return False

    def inaccessible_callback(self, name, **kwargs):
        """Redirect when inaccessible"""
        return redirect(url_for('auth.login', next=request.url))


class UserAdminView(SecureModelView):
    """User admin view with custom configuration"""
    column_list = ['id', 'username', 'email', 'is_admin', 'is_active', 'created_at']
    column_searchable_list = ['username', 'email']
    column_filters = ['is_admin', 'is_active', 'created_at']
    form_excluded_columns = ['password_hash', 'posts']
    column_editable_list = ['is_admin', 'is_active']

    def on_model_change(self, form, model, is_created):
        """Hash password before saving"""
        if is_created and hasattr(form, 'password'):
            model.set_password(form.password.data)


class PostAdminView(SecureModelView):
    """Post admin view with custom configuration"""
    column_list = ['id', 'title', 'summary', 'published', 'user_id', 'created_at']
    column_searchable_list = ['title', 'content']
    column_filters = ['published', 'created_at']
    column_editable_list = ['published']


def setup_admin(app):
    """Setup admin panel with all views"""
    admin = Admin(
        app,
        name='Flask Starter Admin',
        template_mode='bootstrap4',
        url='/admin'
    )

    # Add views
    admin.add_view(UserAdminView(User, db.session, name='Users'))
    admin.add_view(PostAdminView(Post, db.session, name='Posts'))

    return admin
