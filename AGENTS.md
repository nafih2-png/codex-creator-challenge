# Project: AI Consulting Case Simulator

## Objective
Build a portfolio-ready AI application that simulates consulting case interviews and evaluates user responses based on structured problem-solving, clarity, and business judgment.

The application must be simple, usable, and recruiter-ready.

---

## Tech Stack (DO NOT CHANGE)
- Frontend: Next.js (React, TypeScript)
- Backend: Python FastAPI
- API: OpenAI
- Deployment: Vercel (frontend), lightweight backend hosting
- Data storage: None for MVP (use in-memory or static data)

---

## Core Features (MVP ONLY)
- 3 case types:
  - profitability
  - market entry
  - M&A
- User inputs written response
- AI evaluates response using rubric:
  - structure
  - logic
  - clarity
  - business judgment
- Output:
  - score (0–100)
  - strengths
  - weaknesses
  - recommendations

---

## Strict Constraints (IMPORTANT)
- DO NOT add authentication
- DO NOT add payments
- DO NOT add multi-user features
- DO NOT add a database unless explicitly required
- DO NOT over-engineer UI
- DO NOT introduce unnecessary dependencies

---

## Cost Control Rules
- Minimize OpenAI API calls
- Use lower-cost models for development
- Avoid repeated full prompt execution
- Cache or reuse outputs where possible
- Perform calculations (not AI tasks) in Python

---

## Code Style Guidelines
- Write clean, modular, readable code
- Use clear function and variable names
- Keep files small and focused
- Avoid duplication
- Add comments only when necessary

---

## Backend Guidelines
- Use FastAPI with clear endpoints:
  - /cases
  - /evaluate
- Validate inputs (length, empty responses)
- Handle errors gracefully
- Return structured JSON responses

---

## Frontend Guidelines
- Keep UI simple and clean
- Prioritize usability over design complexity
- Use basic components:
  - case selector
  - input box
  - results display
- Ensure responsiveness and readability

---

## AI Prompting Guidelines
- Use a structured rubric-based evaluation
- Always request JSON output
- Keep prompts concise and deterministic
- Avoid unnecessary verbosity

---

## Development Workflow
1. Build backend endpoints first
2. Test endpoints independently
3. Build frontend UI
4. Connect frontend to backend
5. Test full user flow
6. Optimize and polish

---

## Output Quality Standard
The app should demonstrate:
- structured thinking (consulting style)
- clear communication
- practical business recommendations

---

## Definition of Done (MVP)
- User can select a case
- User can submit a response
- AI returns structured evaluation
- Results display correctly in UI
- App runs locally without errors

---

## Future Enhancements (DO NOT BUILD YET)
- user accounts
- voice interaction
- multi-step case simulations
- database integration
- analytics tracking

Only implement after MVP is complete.