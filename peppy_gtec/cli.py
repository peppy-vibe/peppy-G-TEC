"""
CLI module for Peppy G-TEC

Provides command-line interface for running the AlwaysGreen activity monitor.
"""
import sys
import argparse
from .core import AlwaysGreen, DEFAULT_WORKING_PERIODS, DAY_ABBREVIATIONS
from .logo import print_logo, print_instructions


def parse_arguments():
    """
    Parses command-line arguments for configuring the application.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Peppy G-TEC: Keep Teams Status Green! '
                    'Prevents system inactivity during working hours.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog=(
                        'Examples:\n'
                        '  peppy-gtec                                    # Run with defaults (Mon-Fri 08:30-17:30)\n'
                        '  peppy-gtec --time 60                          # Use 60-second timeout\n'
                        '  peppy-gtec --classic                          # Disable colored output\n'
                        '  peppy-gtec --no-logo --no-working-period      # Minimal output\n'
                        '  peppy-gtec --force-enforce                    # Force ENFORCED mode at startup\n'
                        '  peppy-gtec --working-period MON:09:00:00-18:00:00 FRI:09:00:00-14:00:00'
                )
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    parser.add_argument(
        '--working-period',
        nargs='*',
        metavar='DAY:START-END',
        help=(
            'Add working periods in the format DAY:HH:MM:SS-HH:MM:SS. '
            'Multiple periods separated by space. '
            'DAY must be one of: MON TUE WED THU FRI SAT SUN'
        ),
    )
    parser.add_argument(
        '--time',
        type=int,
        default=5,
        metavar='SECONDS',
        help='Timeout period in seconds before inactivity action is taken (default: 5)'
    )
    parser.add_argument(
        '--classic',
        action='store_false',
        default=True,
        dest='modern_output',
        help='Disable colored and emoji output'
    )
    parser.add_argument(
        '--no-logo',
        action='store_false',
        default=True,
        dest='show_logo',
        help='Disable the display of the logo'
    )
    parser.add_argument(
        '--no-instructions',
        action='store_false',
        default=True,
        dest='show_instructions',
        help='Disable the display of instructions'
    )
    parser.add_argument(
        '--no-working-period',
        action='store_false',
        default=True,
        dest='show_working_period',
        help='Disable the display of working periods at startup'
    )
    parser.add_argument(
        '--no-status',
        action='store_false',
        default=True,
        dest='show_status',
        help='Disable the real-time activity status line'
    )
    parser.add_argument(
        '--force-enforce',
        action='store_true',
        dest='force_enforce',
        help='Start in forced ENFORCED mode (ignores working periods until cancelled)'
    )
    parser.add_argument(
        '--force-release',
        action='store_true',
        dest='force_release',
        help='Start in forced RELEASED mode (ignores working periods until cancelled)'
    )

    return parser.parse_args()


def parse_working_periods(period_args):
    """
    Parses working period arguments into a dict.

    Args:
        period_args (list): List of period strings in format DAY:HH:MM:SS-HH:MM:SS

    Returns:
        dict: Working periods keyed by day abbreviation

    Raises:
        SystemExit: If parsing fails
    """
    if period_args is None or len(period_args) == 0:
        return DEFAULT_WORKING_PERIODS

    periods_by_day = {}
    for entry in period_args:
        try:
            abbr, time_range = entry.split(':', 1)
            t_start, t_end = time_range.split('-', 1)
            abbr_upper = abbr.upper()
            if abbr_upper not in DAY_ABBREVIATIONS:
                print(
                    f"Error: Invalid day '{abbr}'. "
                    f"Must be one of: {' '.join(DAY_ABBREVIATIONS)}"
                )
                sys.exit(1)
            periods_by_day.setdefault(abbr_upper, []).append((t_start, t_end))
        except ValueError:
            print(
                f"Error: Invalid working period format: '{entry}'\n"
                "Expected format: DAY:HH:MM:SS-HH:MM:SS\n"
                "Example: MON:08:00:00-17:30:00"
            )
            sys.exit(1)

    return periods_by_day


def main():
    """Entry point: parse arguments, initialize AlwaysGreen, and run."""
    args = parse_arguments()

    if args.force_enforce and args.force_release:
        print('Error: --force-enforce and --force-release cannot be used together.')
        sys.exit(1)

    initial_force_mode = None
    if args.force_enforce:
        initial_force_mode = 'enforce'
    elif args.force_release:
        initial_force_mode = 'release'

    # Parse working periods
    working_periods = parse_working_periods(args.working_period)

    # Initialize AlwaysGreen
    aw = AlwaysGreen(
        timeout_period=args.time,
        working_periods=working_periods,
        modern_output=args.modern_output,
        show_status=args.show_status,
        force_mode=initial_force_mode,
    )

    # Display logo if requested
    if args.show_logo:
        print_logo()

    if args.show_instructions:
        print_instructions()

    # Display working periods if requested
    if args.show_working_period:
        if aw.print_working_periods():
            print('----------------------------------------------')

    # Run the monitor
    try:
        aw.run()
    except KeyboardInterrupt:
        print('\n----------------- TERMINATED -----------------')
        sys.exit(0)


if __name__ == '__main__':
    main()
