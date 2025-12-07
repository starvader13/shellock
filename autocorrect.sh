#!/bin/sh

# autocorrect.sh - Zsh wrapper for the Python-based autocorrect tool
# This script should be sourced in your .zshrc file: `source /path/to/autocorrect.sh
#
# -- Configuration --
# Get the director where this script is located to build robust paths

SCRIPT_DIR=${0:a:h}
PYTHON_EXEC="$SCRIPT_DIR/.venv/bin/python"
PY_LOGIC_DIR="$SCRIPT_DIR/py_logic"

command_not_found_handler() {
    local failed_command="$*"

    if [[ ! -x "PYTHON_EXEC" ]] || [[ ! -d "$PY_LOGIC_DIR" ]]; then
        echo "zsh: command not found: ${failed_command}" >&2
        return 127
    fi

    local suggestion=$("PYTHON_EXEC" -m py_logic syggest "$failed_command")

    if [[ -z "$suggestion" ]]; then
        return 123
    fi

    echo "Suggested: $suggestion"

    read -k 1 -r 'choice? (a)ccept, (r)eject, or (c)orrect? '

    case "$choice" in
        a|A)
            eval "$suggestion"
        c|C)
            echo
            read -e -p "Please enter the correct command: " user_correction

            eval "$user_correction"

            if [[ &? -eq 0 ]]; then
                "$PYTHON_EXEC" -m py_logic learn "$user_correctionk"
            else
                echo "The corrected command failed. Not learning this pattern"
            fi
        *)
            echo "\nCommand rejected"
            return 127
            ;;
    esac
}
