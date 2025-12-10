import shlex
from typing import Optional

from py_logic import file_handler, fuzzy_logic


def get_suggestion(failed_command: str) -> Optional[str]:
    """
    Orchestrates the process of finding a command suggestion.

    This function implements the two-step fuzzy matching:
    1. Find the best matching main command (e.g. "git").
    2. Find the best matching argument pattern (e.g. ["pull", "origin", "main"]).

    Args:
        failed_command: The full command string that the user typed.

    Returns:
        A string of the suggested corrected command, or None if no good suggestion could be found.
    """

    try:
        parts = shlex.split(failed_command)
    except ValueError:
        return None

    if not parts:
        return None

    user_command = parts[0]
    user_args = parts[1:]

    all_data = file_handler.read_and_load_data()
    known_commands = [item["command"] for item in all_data]
    corrected_command = fuzzy_logic.find_best_match(user_command, known_commands)

    # If no correction for the main command, return None.
    # Note: We could potentially suggest the original command with corrected args if main command is perfect,
    # but for now, if the main command is bad, no suggestion.
    if not corrected_command:
        return None

    command_data = next(
        (item for item in all_data if item["command"] == corrected_command), None
    )

    if not command_data or "patterns" not in command_data:
        return " ".join([corrected_command] + user_args)

    known_patterns_for_command = command_data["patterns"]
    
    best_matching_pattern_list = fuzzy_logic.find_best_pattern_match(user_args, known_patterns_for_command)

    final_suggestion_parts = [corrected_command]

    if best_matching_pattern_list:
        final_suggestion_parts.extend(best_matching_pattern_list)
        
        if len(user_args) > len(best_matching_pattern_list):
            extra_user_words = user_args[len(best_matching_pattern_list):]
            final_suggestion_parts.extend(extra_user_words)
    else:
        final_suggestion_parts.extend(user_args)

    return " ".join(final_suggestion_parts).strip()


def learn_pattern(successful_command: str) -> None:
    """
    Adds a new successful command to our knowledge base

    Args:
        successful_command: The full,  correct command string to learn
    """
    try:
        parts = shlex.split(successful_command)
    except ValueError:
        print(
            "Error: Could not learn command due to parsing error (e.g., unclosed quotes)."
        )
        return

    if not parts:
        return

    main_command = parts[0]
    new_pattern = parts[1:]

    all_data = file_handler.read_and_load_data()

    command_found = False
    for item in all_data:
        if item["command"] == main_command:
            command_found = True
            if new_pattern not in item.get("patterns", []):
                item.setdefault("patterns", []).append(new_pattern)
            break

    if not command_found:
        all_data.append({"command": main_command, "patterns": [new_pattern]})

    file_handler.save_data(all_data)
    print(f"Successfully learned new pattern for '{main_command}'.")
