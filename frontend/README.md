# Frontend — Duelo de Respostas

## Executar localmente

1. Inicie a API na raiz do repositório:

   ```powershell
   cd backend
   ..\.venv\Scripts\uvicorn app.main:app --reload
   ```

2. Em outro terminal, instale o Node.js LTS e execute:

   ```powershell
   cd frontend
   npm install
   npm run dev
   ```

O Vite encaminha as chamadas de `/evaluations` para `http://localhost:8000` durante o desenvolvimento.

## Variável de ambiente para deploy

Quando frontend e API estiverem em domínios diferentes, crie um arquivo `.env` em `frontend`:

```env
VITE_API_URL=https://sua-api.exemplo.com
```
