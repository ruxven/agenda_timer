#!/usr/bin/env python3
"""Main entry point for the Agenda Timer application."""
import tkinter
import argparse
from agenda_timer_app import AgendaTimerApp, read_agenda_file


def main():
    """Main function to run the Agenda Timer application."""
    parser = argparse.ArgumentParser(description="Run the Agenda Timer application.")
    parser.add_argument(
        "--agenda",
        "-a",
        type=str,
        help="Path to an agenda file to load on startup",
    )
    args = parser.parse_args()

    # Load initial agenda from file if specified
    initial_agenda = None
    if args.agenda:
        initial_agenda = read_agenda_file(args.agenda)

    root = tkinter.Tk()
    AgendaTimerApp(root, initial_agenda)
    root.mainloop()


if __name__ == "__main__":
    main()
