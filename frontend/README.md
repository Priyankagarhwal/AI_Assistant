# KnowledgeHub AI — Frontend

React 19 + Vite + Tailwind CSS v4 client for the KnowledgeHub AI backend.

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # production build in dist/
npm run lint
```

The backend URL defaults to `http://127.0.0.1:8000`; override it with `VITE_API_URL` in `frontend/.env` (see `.env.example`).

| Page | What it does |
|---|---|
| Dashboard | Counts of workspaces, documents and chats |
| Workspaces | Create / delete workspaces |
| Upload | Upload PDFs to a workspace, list and delete documents |
| Chat | Ask questions; follow-ups use the last few turns; answers show `[n] file, p. X` sources |
| History | Past questions and answers per workspace |
| Summary | Map-reduce summary of a whole workspace |

See the [root README](../README.md) for architecture and setup.
