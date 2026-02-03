"""
Pagination utility for API endpoints
"""
from flask import request, jsonify
from sqlalchemy import or_
from app.models import db


class Pagination:
    """Pagination helper class"""

    def __init__(self, query, page=None, per_page=None, max_per_page=100):
        """
        Initialize pagination

        Args:
            query: SQLAlchemy query object
            page: Page number (default: from request args)
            per_page: Items per page (default: from request args)
            max_per_page: Maximum items per page (default: 100)
        """
        self.query = query
        self.page = page or request.args.get('page', 1, type=int)
        self.per_page = per_page or request.args.get('per_page', 20, type=int)
        self.max_per_page = max_per_page

        # Validate and limit per_page
        if self.per_page < 1:
            self.per_page = 20
        if self.per_page > self.max_per_page:
            self.per_page = self.max_per_page

        # Validate page
        if self.page < 1:
            self.page = 1

    def paginate(self):
        """
        Execute pagination query

        Returns:
            dict with items, pagination metadata
        """
        # Get total count
        total = self.query.count()

        # Calculate pagination
        total_pages = (total + self.per_page - 1) // self.per_page

        # Validate page number
        if self.page > total_pages and total_pages > 0:
            self.page = total_pages

        # Get items
        items = self.query.offset((self.page - 1) * self.per_page).limit(self.per_page).all()

        return {
            'items': items,
            'pagination': {
                'page': self.page,
                'per_page': self.per_page,
                'total': total,
                'total_pages': total_pages,
                'has_next': self.page < total_pages,
                'has_prev': self.page > 1,
                'next_page': self.page + 1 if self.page < total_pages else None,
                'prev_page': self.page - 1 if self.page > 1 else None
            }
        }

    def to_dict(self, serializer=None):
        """
        Convert paginated results to dictionary

        Args:
            serializer: Function to serialize items (default: to_dict)

        Returns:
            dict with items and pagination info
        """
        result = self.paginate()

        if serializer:
            items = [serializer(item) for item in result['items']]
        else:
            items = [item.to_dict() for item in result['items']]

        return {
            'data': items,
            'meta': result['pagination']
        }


def paginate_query(query, serializer=None, max_per_page=100):
    """
    Convenience function to paginate a query

    Args:
        query: SQLAlchemy query object
        serializer: Optional serializer function
        max_per_page: Maximum items per page

    Returns:
        dict with items and pagination metadata
    """
    pagination = Pagination(query, max_per_page=max_per_page)
    return pagination.to_dict(serializer=serializer)


def build_search_params(model, search_fields=None):
    """
    Build search parameters from request args

    Args:
        model: SQLAlchemy model class
        search_fields: List of fields to search in

    Returns:
        tuple of (filters dict, search query, sort field, sort direction)
    """
    filters = {}
    search_query = request.args.get('q', '').strip()
    sort_field = request.args.get('sort', 'created_at')
    sort_dir = request.args.get('order', 'desc')

    # Build filters from request args
    for key, value in request.args.items():
        if key not in ['page', 'per_page', 'q', 'sort', 'order']:
            if hasattr(model, key):
                filters[key] = value

    return filters, search_query, sort_field, sort_dir


def apply_filters(query, model, filters):
    """
    Apply filters to query

    Args:
        query: SQLAlchemy query
        model: Model class
        filters: Dict of field: value filters

    Returns:
        Filtered query
    """
    for field, value in filters.items():
        if hasattr(model, field):
            query = query.filter(getattr(model, field) == value)

    return query


def apply_search(query, model, search_query, search_fields):
    """
    Apply full-text search to query

    Args:
        query: SQLAlchemy query
        model: Model class
        search_query: Search string
        search_fields: List of field names to search

    Returns:
        Filtered query
    """
    if not search_query or not search_fields:
        return query

    search_conditions = []
    for field in search_fields:
        if hasattr(model, field):
            search_conditions.append(
                getattr(model, field).ilike(f'%{search_query}%')
            )

    if search_conditions:
        return query.filter(or_(*search_conditions))

    return query


def apply_sorting(query, model, sort_field, sort_dir):
    """
    Apply sorting to query

    Args:
        query: SQLAlchemy query
        model: Model class
        sort_field: Field name to sort by
        sort_dir: Sort direction ('asc' or 'desc')

    Returns:
        Sorted query
    """
    if not hasattr(model, sort_field):
        sort_field = 'created_at'

    sort_column = getattr(model, sort_field)

    if sort_dir == 'asc':
        return query.order_by(sort_column.asc())
    else:
        return query.order_by(sort_column.desc())
