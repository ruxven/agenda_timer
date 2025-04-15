#!/usr/bin/env python3
"""Agenda Timer Application"""
import tkinter as tk
from tkinter import ttk
import re
import argparse


class TimerWidget(ttk.Frame):
    """A widget representing a timer with a description and countdown functionality."""

    def __init__(self, parent, description, minutes):
        super().__init__(parent)
        self.description = description
        self.total_seconds = minutes * 60
        self.remaining_seconds = self.total_seconds
        self.running = False

        # Configure the widget
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        """A widget to display and control a timer."""
        # Description label
        self.desc_label = ttk.Label(self, text=self.description, wraplength=200)
        self.desc_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=5, pady=2)

        # Time display
        self.time_label = ttk.Label(self, text="00:00")
        self.time_label.grid(row=1, column=0, padx=5)

        # Control buttons
        self.start_button = ttk.Button(self, text="Start", command=self.toggle_timer)
        self.start_button.grid(row=1, column=1, padx=2)

        self.reset_button = ttk.Button(self, text="Reset", command=self.reset_timer)
        self.reset_button.grid(row=1, column=2, padx=2)

    def update_display(self):
        """Update the timer display and apply color coding based on remaining time."""
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.time_label.config(text=time_str)

        # Color coding based on remaining time
        if self.remaining_seconds <= 0:
            self.configure(style="Danger.TFrame")
            self.time_label.configure(foreground="white", background="red")
        elif self.remaining_seconds <= 60:  # 1 minute = 60 seconds
            self.configure(style="Warning.TFrame")
            self.time_label.configure(foreground="black", background="orange")
        else:
            self.configure(style="Normal.TFrame")
            self.time_label.configure(foreground="black", background="lightgreen")

    def toggle_timer(self):
        """Toggle the timer between running and paused states."""
        self.running = not self.running
        self.start_button.config(text="Stop" if self.running else "Start")
        if self.running:
            self.update_timer()

    def update_timer(self):
        """Update the timer countdown and schedule the next update if running."""
        if self.running and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_display()
            self.after(1000, self.update_timer)

    def reset_timer(self):
        """Reset the timer to its initial state."""
        self.running = False
        self.start_button.config(text="Start")
        self.remaining_seconds = self.total_seconds
        self.update_display()


PRESET_AGENDA = """Opening remarks - 5 minutes
Project update - 15 minutes
Q&A session - 10 minutes"""


def read_agenda_file(file_path):
    """Read and return the content of an agenda file."""
    try:
        with open(file_path, "r") as f:
            return f.read().strip()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


class AgendaTimerApp:
    """Main application class for the Agenda Timer."""

    def __init__(self, root, initial_agenda=None):
        self.root = root
        self.root.title("Agenda Timer")
        self.timer_widgets = []
        self.initial_agenda = initial_agenda if initial_agenda else PRESET_AGENDA
        self.agenda_source = "file" if initial_agenda else "preset"

        self.create_widgets()
        self.setup_styles()

    def setup_styles(self):
        """Configure styles for the agenda timer application."""
        style = ttk.Style()
        style.configure("Normal.TFrame", background="white")
        style.configure("Warning.TFrame", background="#fff3e0")
        style.configure("Danger.TFrame", background="#ffebee")

    def create_widgets(self):
        """Create and configure the widgets for the agenda timer application."""
        # Input area
        input_frame = ttk.Frame(self.root)
        input_frame.pack(fill="x", padx=10, pady=5)

        source_text = (
            "Source: File" if self.agenda_source == "file" else "Source: Preset Example"
        )
        ttk.Label(input_frame, text=source_text).pack(anchor="w")

        ttk.Label(
            input_frame, text="Enter agenda items (format: 'Description - XX minutes'):"
        ).pack(anchor="w")

        self.text_input = tk.Text(input_frame, height=10, width=50)
        self.text_input.pack(fill="x", pady=5)

        # Insert initial agenda
        self.text_input.insert("1.0", self.initial_agenda)

        # Parse button
        parse_button = ttk.Button(
            input_frame, text="Create Timers", command=self.parse_agenda
        )
        parse_button.pack(pady=5)

        # Timer container
        self.timer_container = ttk.Frame(self.root)
        self.timer_container.pack(fill="both", expand=True, padx=10, pady=5)

    def parse_agenda(self):
        """Parse the agenda text input and create timer widgets for each entry."""
        # Clear existing timers
        for widget in self.timer_widgets:
            widget.destroy()
        self.timer_widgets.clear()

        # Get text and parse
        text = self.text_input.get("1.0", "end-1c")
        lines = text.split("\n")

        for line in lines:
            if not line.strip():
                continue

            match = re.match(r"(.*?)\s*-\s*(\d+)\s*minutes?", line)
            if match:
                description = match.group(1).strip()
                minutes = int(match.group(2))

                timer_widget = TimerWidget(self.timer_container, description, minutes)
                timer_widget.pack(fill="x", pady=2)
                self.timer_widgets.append(timer_widget)


def main():
    """Main function to initialize and run the Agenda Timer Application."""
    parser = argparse.ArgumentParser(description="Agenda Timer Application")
    parser.add_argument("--input", "-i", type=str, help="Path to agenda input file")
    args = parser.parse_args()

    initial_agenda = None
    if args.input:
        initial_agenda = read_agenda_file(args.input)
        if initial_agenda is None:
            print(f"Failed to read agenda from {args.input}, using preset agenda")

    root = tk.Tk()
    app = AgendaTimerApp(root, initial_agenda)
    root.mainloop()


if __name__ == "__main__":
    main()
