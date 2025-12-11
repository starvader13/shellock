# Shell Command Autocorrect

A smart, learning-based tool for your Zsh shell that automatically detects and suggests corrections for failed commands. Never mistype a `git` command again!

## Features

- **Seamless Correction:** Automatically hooks into your shell to detect failed commands.
- **Corrects Command and Argument Typos:** Fixes both `gti status` and `git sttus`.
- **Interactive Learning:** When it can't find a match, it prompts you to provide the correct command and learns it for next time.
- **Fuzzy Matching:** Uses `rapidfuzz` to intelligently find the closest correction for your typos.
- **User-Controlled:** Provides an interactive `(a)ccept, (r)eject, or (c)orrect?` prompt for all suggestions.
- **Configurable:** Use a simple JSON file to manage learned patterns and an ignore list to prevent the tool from running on specific commands.

## How It Works

This tool uses Zsh's `command_not_found_handler` to intercept failed commands.

1.  When you type a command that Zsh cannot find, the `command_not_found_handler` is triggered.
2.  This handler passes the failed command to a Python script.
3.  The Python script uses fuzzy matching to find the best correction from a list of previously successful commands stored in `autocorrect_aliases.json`.
4.  If a good suggestion is found, it is presented to you with an interactive `(a)ccept, (r)eject, or (c)orrect?` prompt.
5.  If you choose to `(c)orrect`, you can enter the correct command, and if successful, it's automatically saved to `autocorrect_aliases.json` for future use.

## Installation and Setup

This tool is designed for **Zsh**.

1.  **Clone this repository:**
    ```sh
    git clone <repository_url>
    cd auto-correct
    ```

2.  **Set up the Python environment:**
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Edit your `.zshrc` file:**
    Add the following line to your `~/.zshrc` file:

    ```sh
    # Load the autocorrect tool that defines the `command_not_found_handler`
    source /path/to/your/clone/of/auto-correct/autocorrect.sh
    ```
    *Make sure to replace `/path/to/your/clone/of/` with the actual path to where you cloned the repository.*

4.  **Restart your shell** for the changes to take effect.

## Configuration

### Learned Patterns (`autocorrect_aliases.json`)

This file is the brain of the tool. It stores all the successful command patterns the tool has learned. You can manually edit it if you wish.

**Example:**
```json
[
  {
    "command": "git",
    "patterns": [
      ["status"],
      ["add", "-A"]
    ]
  },
  {
    "command": "docker",
    "patterns": [
      ["ps", "-a"]
    ]
  }
]
```

### Ignore List

To prevent the tool from trying to correct commands that are expected to fail (like `grep`), you can add them to the ignore list located inside the `autocorrect.sh` script.

*This will be moved to a more user-friendly configuration file in a future update.*

## Technology

- **Shell:** Zsh
- **Core Logic:** Python 3
- **Fuzzy Matching:** `rapidfuzz` (a fast implementation of Levenshtein Distance)
- **Hooks:** Zsh's `command_not_found_handler`
