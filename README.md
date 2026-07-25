# 🧠 KnowledgeHub AI

An Intelligent RAG (Retrieval-Augmented Generation) platform that lets you upload PDF documents, organize them into workspaces, and chat with your documents using AI.

---

## ✨ Features

- 📁 **Workspace Management** — Create and manage multiple workspaces to organize your documents
- 📄 **PDF Upload** — Upload text-based and image-based (scanned) PDFs
- 🔍 **OCR Support** — Automatically extracts text from image-based PDFs using Tesseract OCR
- 🤖 **AI Chat** — Ask questions about your uploaded documents using LLaMA 3.3 70B via Groq
- 📜 **Chat History** — View all previous conversations per workspace
- 📝 **AI Summary** — Generate summaries of your documents
- 📊 **Dashboard** — Overview of workspaces, documents, and activity

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|---|---|
| FastAPI | REST API framework |
| LangChain | RAG pipeline orchestration |
| Groq (LLaMA 3.3 70B) | LLM for AI responses |
| ChromaDB | Vector database for embeddings |
| sentence-transformers/all-MiniLM-L6-v2 | Text embeddings |
| SQLite + SQLAlchemy | Relational database |
| pypdf | Text-based PDF extraction |
| pytesseract + pdf2image | OCR for image-based PDFs |
| Uvicorn | ASGI server |

### Frontend
| Technology | Purpose |
|---|---|
| React 19 | UI framework |
| Vite 8 | Build tool |
| React Router v7 | Client-side routing |
| Axios | HTTP client |
| Tailwind CSS v4 | Styling |
| Lucide React | Icons |

---

## 📁 Project Structure

```
KnowledgeHub-AI/
├── backend/
│   ├── app/
│   │   ├── api/routes/        # FastAPI route handlers
│   │   ├── config/            # App settings
│   │   ├── core/              # Logger
│   │   ├── database/          # SQLite + ChromaDB setup
│   │   ├── embeddings/        # HuggingFace embedding model
│   │   ├── loaders/           # PDF loader with OCR
│   │   ├── models/            # Pydantic models
│   │   ├── rag/               # RAG pipeline (ingest, retrieve, chat)
│   │   ├── services/          # Business logic
│   │   ├── utils/             # Text splitter
│   │   └── main.py            # FastAPI app entry point
│   ├── uploads/               # Uploaded PDFs (gitignored)
│   ├── storage/               # ChromaDB storage (gitignored)
│   ├── .env.example           # Environment variables template
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/               # Axios instance
│   │   ├── components/        # Navbar, Sidebar, DashboardCard
│   │   ├── layouts/           # MainLayout
│   │   ├── pages/             # Dashboard, Chat, Upload, etc.
│   │   └── routes/            # App routes
│   └── package.json
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 20+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) — install at `C:\Program Files\Tesseract-OCR\`
- [Poppler](https://github.com/oschwartz10612/poppler-windows/releases) — extract at `C:\Program Files\poppler\`
- [Groq API Key](https://console.groq.com) — free to get

---

### Backend Setup

```bash
# 1. Clone the repo
git clone https://github.com/Priyankagarhwal/AI_Assistant.git
cd AI_Assistant/backend

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
copy .env.example .env
# Edit .env and add your GROQ_API_KEY

# 5. Run the backend
uvicorn app.main:app --reload
```

Backend will start at: `http://127.0.0.1:8000`

API Docs available at: `http://127.0.0.1:8000/docs`

---

### Frontend Setup

```bash
# In a new terminal
cd AI_Assistant/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will start at: `http://localhost:5173`

---

### Environment Variables

Create a `.env` file in the `backend/` folder based on `.env.example`:

```env
APP_NAME=KnowledgeHub AI
APP_VERSION=1.0.0
APP_DESCRIPTION=An Intelligent Multi-Source RAG Platform

GROQ_API_KEY=your_groq_api_key_here

MODEL_NAME=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

CHROMA_DB_PATH=storage/chroma
DOCUMENT_PATH=storage/documents
```

---

## 🔄 How It Works

```
User uploads PDF
      ↓
pypdf extracts text (fast)
      ↓
No text found? → OCR via pytesseract (image PDFs)
      ↓
Text split into chunks (LangChain TextSplitter)
      ↓
Chunks embedded → stored in ChromaDB
      ↓
User asks a question
      ↓
Relevant chunks retrieved from ChromaDB
      ↓
LLaMA 3.3 70B (Groq) generates answer from context
      ↓
Answer + chat history saved to SQLite
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Home |
| GET | `/health` | Health check |
| POST | `/workspace` | Create workspace |
| GET | `/workspace` | List all workspaces |
| POST | `/upload` | Upload PDF to workspace |
| GET | `/documents/{workspace_id}` | List documents |
| POST | `/chat` | Ask a question |
| GET | `/history/{workspace_id}` | Get chat history |
| GET | `/summary/{workspace_id}` | Generate summary |
| GET | `/dashboard` | Dashboard stats |

---

## 📄 PDF Support

| PDF Type | Supported |
|---|---|
| Digital text PDF | ✅ |
| Scanned / image PDF | ✅ (via OCR) |
| Mixed text + image | ✅ |
| Handwritten notes | ⚠️ Limited |

---

## 👩‍💻 Author

**Priyanka Garhwal**
B.Tech Computer Engineering — NIT Kurukshetra

[![GitHub](https://img.shields.io/badge/GitHub-priyankagarhwal-black?logo=github)](https://github.com/Priyankagarhwal)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-priyankagarhwal-blue?logo=linkedin)](https://linkedin.com/in/priyankagarhwal)

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).
