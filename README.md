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
git clone https://github.com/yourusername/roams-ai.git
cd roams-ai

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