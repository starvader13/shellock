import shlex
from typing import Optional

from py_logic import file_handler, fuzzy_logic


def get_suggestion(failed_command: str) -> Optional[str]:
    """
    Orchestrates the process of finding a command suggestion

    This function implements the two-step fuzzy matching
    1. Find the best matching main command (e.g. "git")
    2. Find the best matching argument pattern (e.g. ["pull", "origin", "main"])

    Args:
        failed_command: The full command string that the user typed

    Returns:
        A string of the suggested corrected command, or None if no good suggestion could be found
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

    if not corrected_command:
        return None

    command_data = next(
        (item for item in all_data if item["command"] == corrected_command), None
    )

    if not command_data or "patterns" not in command_data:
        return None

    user_args_str = " ".join(user_args)

    pattern_choices = [" ".join(p) for p in command_data["patterns"]]

    best_pattern_str = fuzzy_logic.find_best_match(user_args_str, pattern_choices)

    if not best_pattern_str:
        return " ".join([corrected_command] + user_args)

    final_suggestion = f"{corrected_command} {best_pattern_str}"

    return final_suggestion


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
