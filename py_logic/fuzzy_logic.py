from typing import List, Optional

from rapidfuzz import fuzz, process

SCORE_THRESHOLD = 66


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


def find_best_pattern_match(user_args: List[str], patterns: List[List[str]]) -> Optional[List[str]]:
    """
    Finds the best fuzzy match for a sequence of user arguments from a list of known patterns.

    Args:
        user_args: A list of argument strings provided by the user.
        patterns: A list of known patterns, where each pattern is a list of argument strings.

    Returns:
        The best matching pattern (list of strings) or None if no good match is found.
    """
    if not user_args or not patterns:
        return None

    best_overall_score = -1
    best_matching_pattern = None

    for known_pattern in patterns:
        current_pattern_score_sum = 0
        num_comparisons = 0

        # Score based on arguments that are present in both user_args and known_pattern
        for i in range(min(len(user_args), len(known_pattern))):
            score = fuzz.WRatio(user_args[i], known_pattern[i])
            current_pattern_score_sum += score
            num_comparisons += 1

        # If known_pattern is longer than user_args, penalize the score
        if len(known_pattern) > len(user_args):
            # A simple penalty for missing arguments.
            # Each missing argument reduces the score by a fixed amount or by assuming a 0 score for the missing part.
            current_pattern_score_sum += (len(known_pattern) - len(user_args)) * 0
            num_comparisons += (len(known_pattern) - len(user_args))

        # Calculate the average score for the current pattern
        average_pattern_score = current_pattern_score_sum / num_comparisons if num_comparisons > 0 else 0

        if average_pattern_score > best_overall_score:
            best_overall_score = average_pattern_score
            best_matching_pattern = known_pattern

    if best_overall_score >= SCORE_THRESHOLD:
        return best_matching_pattern
    else:
        return None
