View it live here: https://frontend-lovat-theta-74.vercel.app
Backend is live here: https://quiz.pythonaidev.com/

# Interactive Q&A System with ChatGPT Integration

A modern full-stack web application that serves as an interactive Q&A system using ChatGPT API integration. Built with FastAPI backend and Next.js frontend, and offers a beautiful UI and comprehensive travel documentation assistance.

## 🚀 Features

- **AI-Powered Responses**: Integration with OpenAI ChatGPT API for intelligent responses
- **Real-time Chat Interface**: Modern, responsive chat UI with typing indicators and loading states
- **Query History**: Track and review previous conversations with pagination
- **Travel Documentation Focus**: Specialized prompts for travel visa and documentation queries
- **Responsive Design**: Beautiful UI built with TailwindCSS that works on all devices
- **Error Handling**: Comprehensive error handling and user feedback
- **Performance Optimized**: Fast loading times and efficient API calls

## 🛠 Tech Stack

### Backend
- **Python 3.8+** with **FastAPI** framework
- **OpenAI API** for ChatGPT integration
- **SQLite** database for query storage
- **Pydantic** for data validation
- **Uvicorn** ASGI server

### Frontend
- **Next.js 14** (latest version) with TypeScript
- **TailwindCSS** for styling
- **Framer Motion** for animations
- **Axios** for API calls
- **React Hot Toast** for notifications
- **Lucide React** for icons

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn package manager
- OpenAI API key (free tier compatible)

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/patrickskyman/quiz-system
cd qa-system
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv backend_env

# Activate virtual environment
# On Windows:
backend_env\Scripts\activate
# On macOS/Linux:
source backend_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
sudo nano .env

# Edit .env file and add your OpenAI API key and other 
# OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# The default API URL should work for local development
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4. Get OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add it to the backend `.env` file

## 🚀 Running the Application

### Start the Backend Server

```bash
cd backend

#Create your virtual environement
python3 -m venv backend_env
# Make sure virtual environment is activated
source backend_env/bin/activate  # On Windows: venv\Scripts\activate
#Install requirements
pip3 install -r requirements.txt

# Run the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at: `http://localhost:8000` or `https://quiz.pythonaidev.com`
- API Documentation (Swagger): `http://localhost:8000/docs` or `https://quiz.pythonaidev.com/docs`
- Alternative Documentation (ReDoc): `http://localhost:8000/redoc` or  `https://quiz.pythonaidev.com/redoc`


## 📖 Usage

### Example Queries

The system is optimized for travel documentation queries. Examples:

1. **"Tell me about the travel requirements to the US."**

### API Endpoints

- `POST /api/chat/query` - Submit a question and get AI response
- `GET /api/chat/history` - Retrieve query history with pagination
- `GET /api/chat/stats` - Get system statistics
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation

## 🔧 Configuration

### Backend Configuration (`.env`)

```bash
# Required
OPENAI_API_KEY=openai_api_key_here

# Optional
DATABASE_URL=sqlite:///./qa_system.db
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Frontend Configuration (`.env.local`)

```bash
# Required
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional
NEXT_PUBLIC_APP_NAME="Interactive Q&A System"
NEXT_PUBLIC_ENABLE_ANALYTICS=false
```

## 🚢 Deployment

### Backend Deployment Options

1. **Railway**: Easy Python app deployment
2. **Render**
3. **Heroku**: Classic PaaS platform
4. **DigitalOcean App Platform**: Managed container service

## 📊 Project Structure

```
quiz-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app and configuration
│   │   ├── models.py            # Pydantic models
│   │   ├── database.py          # Database operations
│   │   ├── services/
│   │   │   └── openai_service.py # OpenAI API integration
│   │   └── routers/
│   │       └── chat.py          # Chat endpoints
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Environment variables template
├
└── README.md                    # This file
```

## 🧪 Testing

### Backend Testing

```bash
cd backend
pytest
```

### Frontend Testing

```bash
cd frontend
npm run test
```

## 🔍 API Documentation

The FastAPI backend automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs` or 
- **ReDoc**: `http://localhost:8000/redoc`

---

**Built for the Interactive Q&A System Assessment offerered by Pawa IT**