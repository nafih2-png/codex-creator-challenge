"use client";

import { FormEvent, useEffect, useState } from "react";

type CaseId = "profitability" | "market_entry" | "m_and_a";

type CaseSummary = {
  id: CaseId;
  title: string;
  prompt: string;
};

type CasesResponse = {
  cases: CaseSummary[];
};

type EvaluationResponse = {
  case_id: CaseId;
  score: number;
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
};

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export default function HomePage() {
  const [cases, setCases] = useState<CaseSummary[]>([]);
  const [selectedCaseId, setSelectedCaseId] = useState<CaseId | "">("");
  const [responseText, setResponseText] = useState("");
  const [result, setResult] = useState<EvaluationResponse | null>(null);
  const [loadingCases, setLoadingCases] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadCases() {
      try {
        setLoadingCases(true);
        setError(null);

        const apiResponse = await fetch(`${API_BASE_URL}/cases`, {
          cache: "no-store",
        });
        const data: CasesResponse = await apiResponse.json();

        if (!apiResponse.ok) {
          throw new Error("Unable to load cases.");
        }

        if (!cancelled) {
          setCases(data.cases);
          setSelectedCaseId(data.cases[0]?.id ?? "");
        }
      } catch (loadError) {
        if (!cancelled) {
          setError(
            loadError instanceof Error
              ? loadError.message
              : "Unable to load cases.",
          );
        }
      } finally {
        if (!cancelled) {
          setLoadingCases(false);
        }
      }
    }

    void loadCases();

    return () => {
      cancelled = true;
    };
  }, []);

  const selectedCase =
    cases.find((caseItem) => caseItem.id === selectedCaseId) ?? null;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!selectedCaseId) {
      setError("Please select a case.");
      return;
    }

    try {
      setSubmitting(true);
      setError(null);
      setResult(null);

      const apiResponse = await fetch(`${API_BASE_URL}/evaluate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          case_id: selectedCaseId,
          response: responseText,
        }),
      });

      const data = (await apiResponse.json()) as
        | EvaluationResponse
        | { detail?: string };

      if (!apiResponse.ok) {
        throw new Error("Evaluation failed.");
      }

      setResult(data as EvaluationResponse);
    } catch (submitError) {
      setError(
        submitError instanceof Error
          ? submitError.message
          : "Evaluation failed.",
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="page-shell">
      <div className="page-orb page-orb-left" aria-hidden="true" />
      <div className="page-orb page-orb-right" aria-hidden="true" />

      <section className="hero-card">
        <div className="hero-copy">
          <p className="eyebrow">Recruiter-Ready Demo</p>
          <h1>AI Consulting Case Simulator</h1>
          <p className="hero-text">
            Select a consulting case, write your recommendation, and receive
            structured feedback on your problem solving, clarity, and business
            judgment.
          </p>
        </div>

        <div className="hero-stats" aria-label="MVP highlights">
          <div className="stat-chip">
            <span className="stat-value">3</span>
            <span className="stat-label">Case types</span>
          </div>
          <div className="stat-chip">
            <span className="stat-value">4</span>
            <span className="stat-label">Rubric areas</span>
          </div>
          <div className="stat-chip">
            <span className="stat-value">1</span>
            <span className="stat-label">Simple flow</span>
          </div>
        </div>
      </section>

      <section className="panel-grid">
        <form className="panel" onSubmit={handleSubmit}>
          <div className="panel-heading">
            <h2>Case Response</h2>
            <p>
              Choose a case, structure your recommendation, and submit it for
              evaluation.
            </p>
          </div>

          <label className="field">
            <span>Case Type</span>
            <select
              value={selectedCaseId}
              onChange={(event) => {
                setSelectedCaseId(event.target.value as CaseId);
                setResult(null);
              }}
              disabled={loadingCases || cases.length === 0}
            >
              {loadingCases ? (
                <option>Loading cases...</option>
              ) : (
                cases.map((caseItem) => (
                  <option key={caseItem.id} value={caseItem.id}>
                    {caseItem.title}
                  </option>
                ))
              )}
            </select>
            <small className="field-hint">
              Select one of the consulting scenarios returned by the backend.
            </small>
          </label>

          <div className="prompt-card">
            <div className="prompt-header">
              <p className="prompt-label">Selected Case Prompt</p>
              {selectedCase ? (
                <span className="case-tag">{selectedCase.id}</span>
              ) : null}
            </div>
            <p>{selectedCase?.prompt ?? "No case available."}</p>
          </div>

          <label className="field">
            <span>Written Response</span>
            <textarea
              value={responseText}
              onChange={(event) => setResponseText(event.target.value)}
              placeholder="Write a structured recommendation with key drivers, risks, and next steps."
              rows={12}
            />
            <small className="field-hint">
              A clear, top-down answer usually performs better than a stream of
              ideas.
            </small>
          </label>

          {error ? <p className="message error">{error}</p> : null}

          <button className="submit-button" type="submit" disabled={submitting}>
            {submitting ? "Evaluating..." : "Submit for Evaluation"}
          </button>
        </form>

        <section className="panel result-panel">
          <div className="panel-heading">
            <h2>Evaluation Results</h2>
            <p>
              Structured feedback returned by the backend evaluation endpoint.
            </p>
          </div>

          {result ? (
            <div className="results-card">
              <div className="score-row">
                <div className="score-copy">
                  <p className="result-label">Case ID</p>
                  <p className="result-value">{result.case_id}</p>
                  <p className="result-subtitle">
                    Rubric-based feedback across structure, logic, clarity, and
                    business judgment.
                  </p>
                </div>
                <div className="score-pill">
                  <span>Score</span>
                  <strong>{result.score}</strong>
                </div>
              </div>

              <div className="results-grid">
                <ResultList
                  title="Strengths"
                  items={result.strengths}
                  tone="positive"
                />
                <ResultList
                  title="Weaknesses"
                  items={result.weaknesses}
                  tone="neutral"
                />
                <ResultList
                  title="Recommendations"
                  items={result.recommendations}
                  tone="accent"
                />
              </div>
            </div>
          ) : (
            <div className="empty-state">
              <p className="empty-title">No evaluation yet</p>
              <p>Your feedback will appear here after you submit a response.</p>
            </div>
          )}
        </section>
      </section>
    </main>
  );
}

function ResultList({
  title,
  items,
  tone,
}: {
  title: string;
  items: string[];
  tone: "positive" | "neutral" | "accent";
}) {
  return (
    <div className={`result-section result-section-${tone}`}>
      <h3>{title}</h3>
      <ul>
        {items.map((item) => (
          <li key={`${title}-${item}`}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
