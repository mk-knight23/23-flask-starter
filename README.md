# Flask Starter - Professional Full-Stack Template

A production-ready Flask REST API with React frontend, featuring authentication, database models, and API documentation.

## Features

- Backend
  - Flask 3.1 with Blueprint architecture
  - Flask-RESTX for automatic API documentation
  - JWT authentication with Flask-JWT-Extended
  - SQLAlchemy ORM with database migrations
  - Comprehensive error handling
  - Environment-based configuration
  
- Frontend
  - React 19 with TypeScript
  - Vite 6 for fast development
  - Tailwind CSS v4
  - Lucide React icons
  - Framer Motion animations

- DevOps
  - Gunicorn production server
  - Flask CLI commands
  - pytest testing framework
  - Code quality tools (black, flake8)

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL (production) or SQLite (development)

### One-Line Setup

```bash
./.claude/setup.sh
```

### Manual Setup

#### Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Initialize database
flask init-db

# Seed sample data
flask seed-db

# Run development server
flask run
```

#### Frontend Setup

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## Development

```bash
# Start both servers
make dev

# Or use the dev script
./.claude/scripts/dev.sh
```

Access:
- Frontend: http://localhost:5173
- Backend: http://localhost:5000
- API Docs: http://localhost:5000/api/v1/docs

## Documentation

- [Quick Reference](docs/QUICKREF.md) - Essential commands and endpoints
- [API Documentation](docs/API.md) - Complete API reference
- [Development Workflow](docs/WORKFLOW.md) - Development guide
- [Project Structure](docs/STRUCTURE.md) - Architecture overview
- [RALPH Summary](docs/RALPH_SUMMARY.md) - Implementation details

## Common Commands

```bash
# Database
make db-init      # Initialize database
make db-seed      # Seed sample data
make db-reset     # Reset database

# Testing
make test         # Run tests
make test-cov     # With coverage

# Code Quality
make format       # Format code
make lint         # Check linting

# Production
make build        # Build for production
make run          # Run with Gunicorn
```

## API Documentation

### Interactive Docs
- Swagger UI: `http://localhost:5000/api/v1/docs`
- ReDoc: `http://localhost:5000/api/v1/redoc`

### Key Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user

#### Users
- `GET /api/v1/users` - List users
- `GET /api/v1/users/:id` - Get user
- `PUT /api/v1/users/:id` - Update user
- `DELETE /api/v1/users/:id` - Delete user

#### Posts
- `GET /api/v1/posts` - List posts
- `GET /api/v1/posts/:id` - Get post
- `POST /api/v1/posts` - Create post
- `PUT /api/v1/posts/:id` - Update post
- `DELETE /api/v1/posts/:id` - Delete post

See [API.md](docs/API.md) for complete API reference.

## Project Structure

```
48-starter-flask/
├── app/                   # Flask application
│   ├── blueprints/       # Route blueprints (main, api, auth)
│   ├── models/           # Database models
│   ├── utils/            # Utilities (validators, decorators)
│   └── commands.py       # CLI commands
├── tests/                # Test suite
├── docs/                 # Documentation
├── .claude/              # Automation scripts
└── src/                  # React frontend
```

See [STRUCTURE.md](docs/STRUCTURE.md) for detailed architecture.

## Environment Variables

```bash
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=sqlite:///app.db

# JWT
JWT_SECRET_KEY=your-jwt-secret

# CORS
CORS_ORIGINS=http://localhost:5173
```

## Production Deployment

### Using Gunicorn

```bash
# Build frontend
npm run build

# Start production server
gunicorn -c gunicorn_config.py app:app
```

### Using Docker

```bash
docker-compose up -d
```

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test
pytest tests/test_auth.py
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Write tests for your feature
4. Ensure tests pass
5. Submit a pull request

## Code Quality

- Python: PEP 8 compliant (black + flake8)
- TypeScript: ESLint + Prettier
- Test coverage: 80%+

## License

MIT License - see LICENSE file for details

## Author

**Kazi Musharraf**
- GitHub: [@mk-knight23](https://github.com/mk-knight23)

## Live Demo

- **Cloudflare Pages**: https://48-starter-flask.pages.dev ✓
- **Vercel**: https://48-starter-flask.vercel.app *(backend requires Python hosting)*
- **GitHub**: https://github.com/mk-knight23/48-starter-flask

---

Last Updated: 2026-02-02
