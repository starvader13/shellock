#!/bin/zsh

# autocorrect.sh - Zsh wrapper for the Python-based autocorrect tool
# This script should be sourced in your .zshrc file: `source /path/to/autocorrect.sh
#
# -- Configuration --

# Get the director where this script is located to build robust paths
SCRIPT_DIR=${0:a:h}
PYTHON_EXEC="$SCRIPT_DIR/.venv/bin/python"
PY_LOGIC_DIR="$SCRIPT_DIR/py_logic"

# -- Colors --
C_YELLOW='\e[33m'
C_CYAN='\e[36m'
C_RED='\e[31m'
C_GREEN='\e[32m'
C_RESET='\e[0m'

command_not_found_handler() {
    local failed_command="$*"

    if [[ ! -x "$PYTHON_EXEC" ]] || [[ ! -d "$PY_LOGIC_DIR" ]]; then
        echo "zsh: command not found: ${failed_command}" >&2
        return 127
    fi

    local suggestion=$("$PYTHON_EXEC" -m py_logic suggest "$failed_command")

    if [[ -z "$suggestion" ]]; then
        echo "zsh: command not found: ${failed_command}" >&2
        return 127
    fi

    echo -e "${C_YELLOW}Suggested: ${C_CYAN}$suggestion${C_RESET}"
    echo -ne "${C_CYAN}(${C_RED}a${C_CYAN})ccept, (${C_RED}r${C_CYAN})eject, or (${C_RED}c${C_CYAN})orrect? ${C_RESET}"
    read -k 1 -r choice


    case "$choice" in
        a|A)
            eval "$suggestion"
            ;;
        c|C)
            echo
            echo -ne "${C_CYAN}Please enter the correct command: ${C_RESET}"
            read -r user_correction < /dev/tty

            echo
            eval "$user_correction"

            if [[ $? -eq 0 ]]; then
                "$PYTHON_EXEC" -m py_logic learn "$user_correction"
            else
                echo -e "${C_RED}The corrected command failed. Not learning this pattern${C_RESET}"
            fi
            ;;
        *)
            echo -e "${C_RED}\nCommand rejected${C_RESET}"
            return 127
            ;;
    esac
}
