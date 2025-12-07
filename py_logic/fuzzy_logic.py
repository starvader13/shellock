from typing import List, Optional

from rapidfuzz import fuzz, process

SCORE_THRESHOLD = 75


def find_best_match(query: str, choices: List[str]) -> Optional[str]:
    """
    Finds the best fuzzy match for a query string from a list of choice

    Args:
        query: The misspelled string to correct (e.g. "gti")
        choices: A list of valid strings to match against (e.g. ["git", "ls"])
    """

    if not query or not choices:
        return None

    best_match = process.extractOne(query, choices, scorer=fuzz.WRatio)

    if not best_match:
        return None

    choice, score, _ = best_match

    if score >= SCORE_THRESHOLD:
        return choice
    else:
        return None
