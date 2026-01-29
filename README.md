# Chat-GPT Clone

AI-powered chat app with Groq LLM & Pinecone memory management.

## Quick Start

### 1. Setup
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure
```powershell
cp .env.example .env
```

Edit `.env` with your API keys:
- **GROQ_API_KEY** → https://console.groq.com
- **PINECONE_API_KEY** → https://app.pinecone.io
- **PINECONE_INDEX_NAME** → `chat-memory`
- **PINECONE_ENVIRONMENT** → Your environment from Pinecone

### 3. Create Pinecone Index
1. Go to https://app.pinecone.io
2. Create new index:
   - Name: `chat-memory`
   - Dimension: `384`
   - Metric: `Cosine`
   - Pod: `Starter` (free)

### 4. Run
```powershell
python main.py
```
Open: http://localhost:5000

## Features
- Real-time chat with AI
- Semantic memory (similar messages retrieval)
- Session management
- Context-aware responses
- Fast Groq LLM inference

## Project Structure
```
app/
├── routes/          # API endpoints
├── services/        # LLM & Chat logic
├── utils/           # Embeddings & Memory
├── templates/       # HTML pages
└── static/          # CSS styles

config/config.py     # Configuration
main.py              # Entry point
```

## API Endpoints
```
POST   /api/chat/session              
POST   /api/chat/message              
GET    /api/chat/history/<session_id> 
DELETE /api/chat/clear/<session_id>   
```

## Deploy to Render

1. Push to GitHub
2. Go to https://dashboard.render.com
3. Create "Web Service" + Connect GitHub repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `python main.py`
6. Set environment variables (GROQ_API_KEY, PINECONE_API_KEY, etc.)
7. Deploy

## Tech Stack
- Flask (Backend)
- Groq API (LLM)
- Pinecone (Vector DB)
- Sentence Transformers (Embeddings)
- HTML/CSS/JS (Frontend)
