# Quiz System - AI-Powered Q&A Platform

This is a modern web application for AI-powered Q&A using ChatGPT integration, built with Next.js frontend and FastAPI backend and serves as an AI-Powered Travel Documentation Helper.

## 🏗️ Project Structure

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
├   ├── README.md                # Backend README
│   └── .env                    # Environment variables template (The file is referenced here; 3. **Configure environment variables:**)
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx       # Root layout
│   │   │   ├── page.tsx         # Home page
│   │   │   └── globals.css      # Global styles
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx # Main chat component
│   │   │   └── QueryHistory.tsx  # History sidebar
│   │   └── lib/
│   │       └── api.ts           # API utilities
│   ├── package.json             # Node.js dependencies
│   ├── tailwind.config.js       # Tailwind configuration
│   └── README.md                # Frontedn README file
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- OpenAI API Key

### Frontend Setup
```bash
Refer to Frontend README 
```

### Backend Setup
```bash
Refer to Backend README 
```

## 🌐 Deployment

### Frontend (Vercel)
The frontend is configured for Vercel deployment. Connect your GitHub repository to Vercel and it will automatically deploy from the `frontend/` directory.

**Vercel Configuration:**
- Root Directory: `frontend`
- Build Command: `npm run build`
- Output Directory: `.next`

### Backend (VPS)
The backend is designed to run on a VPS with the following setup:

1. **Clone the repository:**
```bash
git clone https://github.com/patrickskyman/quiz-system
cd quiz-system/backend
```

2. **Set up Python environment:**
```bash
python3 -m venv app_env
source app_env/bin/activate
pip3 install -r requirements.txt
```
3. **Configure environment variables:**
```bash
sudo nano .env
# Edit .env with the OpenAI API key and other settings as shown below
# OpenAI Configuration
OPENAI_API_KEY=replace_with_your_api_key_here

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Environment
ENVIRONMENT=development

# Logging
LOG_LEVEL=INFO

# CORS Origins (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Rate Limiting (requests per minute)
RATE_LIMIT=60

# Security
SECRET_KEY=******
ALGORITHM=HS256

# Production Database (PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost/dbname 


# Optional: Redis for caching
# REDIS_URL=redis://localhost:6379/0
```

4. **Run with Gunicorn (production):**
```bash
gunicorn --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 app.main:app
```

5. **Set up reverse proxy (Nginx):**
```nginx
server {
    server_name your_domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/your_name/quiz-system/backend;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn-quiz-system.sock;
    }


}
```

## 🔧 Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```


## 📦 Development Workflow

1. **Make changes** in either frontend or backend
## Step 1 - Committing Changes in the Backend (Main Repo)
```bash
git add .
git commit -m "Update backend logic ..."
git push origin main
```
## Step 2 - Committing Changes in the Frontend (Submodule)
```bash
cd frontend
git add .
git commit -m "Update frontend UI"
git push origin main
```
## Step 3 - Update Submodule Reference in Main Repo
```bash
cd ..
git add frontend
git commit -m "Update frontend submodule reference"
git push origin main
```

2. **Test locally** using the setup commands above
3. **Commit and push** to GitHub
4. **Vercel automatically deploys** the frontend
5. **Automatically deploy** backend changes to your VPS once the changes are pushed to Github

## 🔄 Continuous Deployment

### Frontend (Automatic)
- Vercel automatically detects changes in the `frontend/` directory
- Deploys on every push to main branch
- Preview deployments for pull requests

### Backend (Manual)
- The changes reflect directly to the server since the GitHub Actions have been integrated successfully
check - the file
```bash
.github/workflows/deploy.yml
```

## 🛠️ Development Scripts

## 📝 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both frontend and backend
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the API documentation
2. Review the logs in both frontend and backend
3. Create an issue in the GitHub repository 