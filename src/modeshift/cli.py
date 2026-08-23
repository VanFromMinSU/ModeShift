import argparse


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="modeshift",
        description="Windows system profile manager.",
    )

    parser.add_argument(
        "mode",
        nargs="?",
        choices=["gaming", "balanced", "battery", "restore", "status"],
        help="ModeShift operation to perform.",
    )

    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    if args.mode is None:
        parser.print_help()
        return

    print(f"Selected operation: {args.mode}")