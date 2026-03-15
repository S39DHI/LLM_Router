import re
from typing import Set, List

# --- keyword signals used to estimate query difficulty ---

COMPLEX_KEYWORDS: Set[str] = {
    "architecture", "distributed", "scalable", "pipeline",
    "microservices", "kubernetes", "optimization",
    "performance", "algorithm", "system"
}

REASONING_WORDS: Set[str] = {
    "why", "how", "explain", "analyze", "evaluate"
}

COMPARISON_WORDS: Set[str] = {
    "compare", "difference", "vs", "versus"
}

TASK_WORDS: Set[str] = {
    "design", "build", "implement", "create", "develop"
}

def tokenize(text: str) -> List[str]:
    """Extract lowercase words from text."""
    return re.findall(r"\b\w+\b", text.lower())

def classify_complexity(question: str) -> str:
    """
    Classify the complexity of a query using heuristic signals.

    The classifier assigns a difficulty score based on:
    - query length
    - reasoning words
    - comparison words
    - task/instruction words
    - technical/system keywords
    - multi-part question structure
    """

    q = question.lower().strip()
    words = tokenize(q)
    word_count = len(words)

    score = 0

    # --- length heuristic ---
    if word_count > 10:
        score += 1
    if word_count > 18:
        score += 1

    # --- reasoning signals ---
    if any(w in REASONING_WORDS for w in words):
        score += 1

    # --- comparison questions ---
    if any(w in COMPARISON_WORDS for w in words):
        score += 1

    # --- task/design instructions ---
    if any(w in TASK_WORDS for w in words):
        score += 1

    # --- technical complexity terms ---
    if any(w in COMPLEX_KEYWORDS for w in words):
        score += 2

    # --- multi-part query detection ---
    if " and " in q or "," in q:
        score += 1

    # --- final classification ---
    if score <= 1:
        return "simple"
    elif score <= 3:
        return "medium"
    else:
        return "complex"
