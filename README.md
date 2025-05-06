# CataractDetect AI Platform

An AI-powered web application for cataract detection and medical consultation using deep learning models and natural language processing.

## Features

- 🔍 Cataract Detection using dual AI models:
  - LeNet5 (128x128 grayscale images)
  - MobileNetV2 (224x224 RGB images)
- 💬 AI Medical Consultation:
  - Powered by DeepSeek for contextual medical advice
  - Medical knowledge base integration (RAG with LangChain)
  - Smart FAQ system
- 👤 User Management:
  - Secure authentication with JWT
  - Profile management
  - Phone number verification
- 🎨 Modern UI/UX:
  - Responsive design with Vuetify
  - Real-time chat interface
  - Image upload preview
  - Interactive FAQ system

## Tech Stack

### Frontend
- Vue.js 3 with Composition API
- Vuetify for UI components
- Vue Router for navigation
- Pinia for state management

### Backend
- **FastAPI** (Python) for REST API
- **Async SQLAlchemy** for database ORM
- **PostgreSQL** database
- **JWT authentication**
- **Controller-based structure** for clean separation of business logic

### AI/ML
- TensorFlow/Keras for ML models
- DeepSeek for medical consultation
- LangChain + FAISS for medical knowledge vectorstore (RAG)

## Prerequisites

- Node.js >= 16.x
- PostgreSQL >= 14.x
- Python >= 3.8 (for ML models & backend)
- npm or yarn

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cataract-detection.git
cd cataract-detection
```

2. Install frontend dependencies:
```bash
cd app/cataract_detect
npm install
```

3. Install backend dependencies:
```bash
cd ../../backend
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Backend .env
cp .env.example .env
# Edit .env with your database credentials, JWT secret, and model paths
```

5. Initialize database:
```bash
# Run Alembic migrations
alembic upgrade head
```

6. Start development servers:
```bash
# Backend (from backend directory)
uvicorn main:app --reload

# Frontend (from app/cataract_detect directory)
npm run dev
```

## Project Structure

```
CataractDetection/
├── app/
│   └── cataract_detect/      # Frontend Vue.js application
│       ├── src/
│       │   ├── components/   # Reusable Vue components
│       │   ├── composables/  # Vue composition functions
│       │   ├── layouts/      # Page layouts
│       │   ├── pages/        # Vue pages/routes
│       │   ├── plugins/      # Vue plugins
│       │   ├── router/       # Vue router configuration
│       │   └── stores/       # Pinia stores
├── backend/
│   ├── controllers/          # Business logic (controllers)
│   ├── models.py             # Database models
│   ├── auth.py, images.py    # API routes (now call controllers)
│   ├── uploads/              # Image uploads
│   └── ...
└── ML/
    ├── models/              # Trained ML models
    └── training/            # Model training scripts
```

### Backend Refactor Note
- The backend now uses a **controller-based structure**. All business logic for users, images, etc. is in `backend/controllers/`. Route files (e.g., `auth.py`) simply call these controller functions for better organization and maintainability.

## API Documentation

See [API_DOCS.md](./API_DOCS.md) for detailed API documentation.

## Testing

See [TESTING.md](./TESTING.md) for testing documentation and guidelines.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 