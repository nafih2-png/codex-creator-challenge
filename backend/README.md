# Backend

Minimal FastAPI backend for the AI Consulting Case Simulator MVP.

## Endpoints

- `GET /cases`
- `POST /evaluate`

## Local Run

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Notes

- If `OPENAI_API_KEY` is set, `/evaluate` uses OpenAI with structured JSON output.
- If no API key is set, the backend falls back to a deterministic local evaluator so the MVP can still be exercised during development.
