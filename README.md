# Roams AI - Text Generation API

FastAPI-based REST API for text generation using Hugging Face models, developed as a technical assessment project.

## 🚀 Features

- Text generation with GPT-2 model from Hugging Face
- FastAPI REST endpoints
- JWT authentication
- Request history tracking (SQLite)
- Parameter customization (length, temperature, top-p)
- API documentation (Swagger/OpenAPI)
- Docker support

## 📋 Requirements

- Python 3.8+
- Docker (optional)
- Dependencies in `requirements.txt`

## ⚙️ Installation

### Using Docker

```bash
# Clone repository
git clone https://github.com/GuillermoLB/Prueba-tecnica-Roams.git
cd Prueba-tecnica-Roams

# Setup environment
cp .env.template .env

# Start with Docker
make dev
```

### Manual Setup

```bash
# Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup database
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

## 🔧 Usage

### API Documentation

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Example Requests

1. **Create User**:

    ```bash
    curl -X POST http://localhost:8000/users \
      -H "Content-Type: application/json" \
      -d '{"username": "test", "password": "password123"}'
    ```

2. **Get Token**:

    ```bash
    curl -X POST http://localhost:8000/token \
      -d "username=test&password=password123"
    ```
3. **Configure Model Parameters**:

    ```bash
    curl -X PUT http://localhost:8000/models \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
    "max_length": 100,
    "temperature": 0.7,
    "top_p": 0.9
    }'
    ```
4. **Generate Text**:

    ```bash
    curl -X POST http://localhost:8000/text_generations \
      -H "Authorization: Bearer YOUR_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"prompt": "Once upon a time"}'
    ```

## 🔍 Implementation Details

### Architecture

The project follows a loosely-coupled architecture with clear separation of concerns:
- **Domain Layer**: Models and schemas in [`app/domain/`](app/domain/)
- **Repository Layer**: Database operations in [`app/repos/`](app/repos/)
- **Service Layer**: Business logic in [`app/services/`](app/services/)
- **API Layer**: REST endpoints in [`app/routes/`](app/routes/)
- **ML Layer**: Model integration in [`app/ml/`](app/ml/)

This design allows for:
- Easy testing and maintenance
- Flexibility to change implementations
- Clear dependency flow
- Separation between business logic and infrastructure

### Database

Uses SQLite through SQLAlchemy ORM with three main tables:
- `users`: Authentication and user management
- `models`: AI model configurations
- `text_generations`: History of generated texts

Migrations are handled by Alembic, making database changes trackable and reversible.

### Logging System

Comprehensive logging implemented in [`app/core/log_config.py`](app/core/log_config.py):
- Request/response logging with unique IDs
- ML model operations logging
- Configurable log levels via environment variables
- Structured format for easy parsing

### Model Focus

The project emphasizes REST API design and software architecture over model complexity:
- Uses lightweight GPT-2 model for quick demonstrations
- Easily switchable to other Hugging Face models
- Focus on API usability and maintainability

### Environment Variables

Configuration in [`.env`](.env) includes:
- **Database**: 
  - `DB_NAME`: SQLite database name
- **Model Settings**:
  - `MODEL_NAME`: Name for tracking configurations
  - `LLM_ID`: Hugging Face model identifier
- **Security**:
  - `SECRET_KEY`: JWT signing key, it is convenient to generate a new one with `openssl rand -hex 32`
  - `ACCESS_TOKEN_EXPIRE_MINUTES`: Token validity period
  - `ALGORITHM`: JWT algorithm (HS256)
- **Logging**:
  - `LOG_LEVEL`: Logging verbosity
  - `DISABLE_LOGGERS`: Logger control flag

## 🛠️ Development

### Make Commands

- `make up`: Start containers
- `make down`: Stop containers
- `make build`: Build images
- `make logs`: View logs
- `make shell`: Container shell
- `make migrate`: Run migrations
- `make dev`: Full setup

### Project Structure

```plaintext
roams-ai/
├── alembic/           # Database migrations
├── app/
│   ├── core/         # Configuration
│   ├── domain/       # Models & schemas
│   ├── error/        # Error handling
│   ├── ml/           # ML components
│   ├── repos/        # DB repositories
│   ├── routes/       # API endpoints
│   ├── services/     # Business logic
│   └── utils/        # Utilities
```

## 📄 License

MIT License - see [LICENSE](LICENSE) for details