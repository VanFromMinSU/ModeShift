import argparse

from .system import (
    get_battery_info,
    get_performance_info,
    get_system_info,
)


def create_parser() -> argparse.ArgumentParser:
    """Create the ModeShift command-line argument parser."""
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


def display_status() -> None:
    """Display the current system status."""
    system = get_system_info()
    performance = get_performance_info()
    battery = get_battery_info()

    print()
    print("ModeShift Status")
    print("=" * 40)

    print()
    print("System")
    print("-" * 40)
    print(f"OS:               {system['windows_version']}")
    print(f"Architecture:     {system['machine']}")
    print(f"CPU:              {system['processor']}")
    print(
        f"CPU Cores:        "
        f"{system['physical_cpu_count']} physical / "
        f"{system['cpu_count']} logical"
    )
    print(f"Memory:           {system['memory_total_gb']} GB")

    print("GPU:")
    if system["gpu_names"]:
        for gpu in system["gpu_names"]:
            print(f"                  {gpu}")
    else:
        print("                  Unknown")

    print()
    print("Performance")
    print("-" * 40)
    print(f"CPU Usage:        {performance['cpu_usage_percent']}%")
    print(f"Memory Usage:     {performance['memory_usage_percent']}%")
    print(f"Memory Used:      {performance['memory_used_gb']} GB")
    print(f"Memory Available: {performance['memory_available_gb']} GB")

    print()
    print("Power")
    print("-" * 40)

    if battery is None:
        print("Battery:          Not available")
    else:
        power_source = "AC Power" if battery["plugged_in"] else "Battery"

        print(f"Battery:          {battery['percent']}%")
        print(f"Power Source:     {power_source}")

        if battery["seconds_remaining"] >= 0:
            minutes = battery["seconds_remaining"] // 60
            hours = minutes // 60
            remaining_minutes = minutes % 60

            print(
                f"Time Remaining:   "
                f"{hours}h {remaining_minutes:02d}m"
            )
        else:
            print("Time Remaining:   Unknown")


def main() -> None:
    """Run the ModeShift CLI."""
    parser = create_parser()
    args = parser.parse_args()

    if args.mode is None:
        parser.print_help()
        return

    if args.mode == "status":
        display_status()
        return

    print(f"Selected operation: {args.mode}")