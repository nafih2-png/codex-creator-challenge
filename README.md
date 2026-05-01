# AI Consulting Case Simulator

An AI-powered web application that simulates consulting case interviews and evaluates responses based on structured problem-solving, clarity, and business judgment.

## Features
- Profitability, Market Entry, and M&A case types
- AI-based evaluation with structured scoring
- Feedback on strengths, weaknesses, and improvements
- Executive-style recommendations

## Tech Stack
- Frontend: Next.js (TypeScript)
- Backend: FastAPI (Python)
- AI: OpenAI API
- Styling: Custom CSS (lightweight, no extra dependencies)

## How It Works
1. Select a case type
2. Enter your response
3. Receive structured evaluation:
   - Score
   - Strengths
   - Weaknesses
   - Recommendations

## Why This Project
This project demonstrates:
- Structured problem solving (consulting-style thinking)
- Data-driven evaluation
- Full-stack development
- Practical AI application for business decision-making

## Run Locally

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

Then open [http://localhost:3000](http://localhost:3000)
