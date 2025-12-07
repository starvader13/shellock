import argparse
import sys

from py_logic import core


def main():
    """
    Defined the command-line interfac4e for the autocorrection tool and
    routes commands to the appropriate core logic function
    """

    parser = argparse.ArgumentParser(
        prog="autocorrect_logic",
        description="Core logic for the commnd autocorrect tool",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_suggest = subparsers.add_parser(
        "suggest", help="Get a suggestion for the failed command"
    )
    parser_suggest.add_argument(
        "failed_command", type=str, help="The full string of the failed comand"
    )

    parser_learn = subparsers.add_parser(
        "learn", help="Learn a new pattern from a successful command"
    )
    parser_learn.add_argument(
        "successful_command", typr=str, help="The full string of the successful command"
    )

    args = parser.parse_args()

    if args.command == "suggest":
        suggestion = core.get_suggestion(args.failed_command)
        if suggestion:
            print(suggestion)
            sys.exit(0)
        else:
            sys.exit(1)

    elif args.command == "learn":
        core.learn_pattern(args.successful_command)
        sys.exit(0)


if __name__ == "__main__":
    main()
