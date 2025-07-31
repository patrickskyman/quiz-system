# Quiz System - AI-Powered Q&A Platform

A modern web application for AI-powered Q&A using ChatGPT integration, built with Next.js frontend and FastAPI backend.

## 🏗️ Project Structure

```
quiz-system/
├── frontend/          # Next.js React application
│   ├── src/
│   ├── package.json
│   └── ...
├── backend/           # FastAPI Python application
│   ├── app/
│   ├── requirements.txt
│   └── ...
├── .gitignore         # Root-level gitignore
└── README.md          # This file
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- OpenAI API Key

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
python -m venv app_env
source app_env/bin/activate  # On Windows: app_env\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🌐 Deployment

### Frontend (Vercel)
The frontend is configured for Vercel deployment. Simply connect your GitHub repository to Vercel and it will automatically deploy from the `frontend/` directory.

**Vercel Configuration:**
- Root Directory: `frontend`
- Build Command: `npm run build`
- Output Directory: `.next`

### Backend (VPS)
The backend is designed to run on a VPS with the following setup:

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd quiz-system/backend
```

2. **Set up Python environment:**
```bash
python -m venv app_env
source app_env/bin/activate
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
cp env.example .env
# Edit .env with your OpenAI API key and other settings
```

4. **Run with Gunicorn (production):**
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

5. **Set up reverse proxy (Nginx):**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔧 Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)
```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./qa_system.db
```

## 📦 Development Workflow

1. **Make changes** in either frontend or backend
2. **Test locally** using the setup commands above
3. **Commit and push** to GitHub
4. **Vercel automatically deploys** the frontend
5. **Manually deploy** backend changes to your VPS

## 🔄 Continuous Deployment

### Frontend (Automatic)
- Vercel automatically detects changes in the `frontend/` directory
- Deploys on every push to main branch
- Preview deployments for pull requests

### Backend (Manual)
- SSH into your VPS
- Pull latest changes: `git pull origin main`
- Restart the service: `sudo systemctl restart your-app`

## 🛠️ Development Scripts

### Root Level (Optional)
You can add these scripts to the root `package.json` for convenience:

```json
{
  "scripts": {
    "dev:frontend": "cd frontend && npm run dev",
    "dev:backend": "cd backend && uvicorn app.main:app --reload",
    "dev": "concurrently \"npm run dev:frontend\" \"npm run dev:backend\"",
    "build:frontend": "cd frontend && npm run build",
    "install:all": "cd frontend && npm install && cd ../backend && pip install -r requirements.txt"
  }
}
```

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