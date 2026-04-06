from dataclasses import dataclass


@dataclass(frozen=True)
class CaseDefinition:
    id: str
    title: str
    prompt: str


CASE_DEFINITIONS: tuple[CaseDefinition, ...] = (
    CaseDefinition(
        id="profitability",
        title="Profitability Decline at a Regional Airline",
        prompt=(
            "A regional airline has seen profits fall by 25% over the last year "
            "despite stable revenue. The CEO wants a recommendation on what to "
            "investigate first and what actions to consider."
        ),
    ),
    CaseDefinition(
        id="market_entry",
        title="US Coffee Chain Entering India",
        prompt=(
            "A mid-sized US coffee chain is considering entering the Indian market. "
            "The leadership team wants an initial recommendation on whether to enter "
            "and what factors matter most."
        ),
    ),
    CaseDefinition(
        id="m_and_a",
        title="Software Company Acquisition Decision",
        prompt=(
            "A B2B software company is evaluating whether to acquire a smaller AI "
            "analytics startup. The board wants a recommendation on whether the deal "
            "creates value and what key risks should be assessed."
        ),
    ),
)


def get_case_by_id(case_id: str) -> CaseDefinition | None:
    return next((case for case in CASE_DEFINITIONS if case.id == case_id), None)
