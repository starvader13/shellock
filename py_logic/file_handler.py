import json
from pathlib import Path
from typing import Any, Dict, List

CONFIG_FILE = Path(__file__).parent.parent / "autocorrect_aliases.json"


def read_and_load_data() -> List[Dict[str, Any]]:
    """
    Safely loads and parses the JSON data from the configuration file

    Returns:
        A list of dictinoaries representing the command patterns
        Returns an empty list if the file doesn't exists or is invalid
    """

    if not CONFIG_FILE.exists():
        return []

    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from {CONFIG_FILE}. Starting fresh.")
        return []
    except IOError as e:
        print(f"Warning: Could not read file {CONFIG_FILE}: {e}")
        return []


def save_data(data: List[Dict[str, Any]]):
    """
    Safely writes the given data structure back to the JSON configuration file

    Args:
        data: The python list of dictionaries to save
    """
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error: Could not write to file {CONFIG_FILE}: {e}")
