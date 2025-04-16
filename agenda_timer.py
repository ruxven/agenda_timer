#!/usr/bin/env python3
"""Agenda Timer Application"""
import tkinter
import tkinter.ttk
import tkinter.font
import tkinter.filedialog
import re
import argparse


class TimerWidget(tkinter.ttk.Frame):
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
        """A widget to display and control a timer."""  # Get default font and its size
        # Get default font and its size
        default_font = tkinter.font.nametofont("TkDefaultFont")
        default_size = default_font.cget("size")

        # Create timer font with doubled size
        timer_font = default_font.copy()
        timer_font.configure(size=default_size * 2)

        # Time display with doubled font size
        self.time_label = tkinter.ttk.Label(self, text="00:00", font=timer_font)
        # Description label
        self.desc_label = tkinter.ttk.Label(self, text=self.description, wraplength=200)
        self.desc_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=5, pady=2)

        # Time display with doubled font size
        self.time_label = tkinter.ttk.Label(self, text="00:00", font=timer_font)
        self.time_label.grid(row=1, column=0, padx=5)

        # Control buttons
        self.start_button = tkinter.ttk.Button(
            self, text="Start", command=self.toggle_timer
        )
        self.start_button.grid(row=1, column=1, padx=2)

        self.reset_button = tkinter.ttk.Button(
            self, text="Reset", command=self.reset_timer
        )
        self.reset_button.grid(row=1, column=2, padx=2)

    def update_display(self):
        """Update the timer display and apply color coding based on remaining time and state."""
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.time_label.config(text=time_str)

        # Color coding based on timer state and remaining time
        if not self.running:
            # Inactive state
            self.configure(style="Inactive.TFrame")
            self.time_label.configure(foreground="#444444", background="#e0e0e0")
        elif self.remaining_seconds <= 0:
            # Danger state
            self.configure(style="Danger.TFrame")
            self.time_label.configure(foreground="white", background="red")
        elif self.remaining_seconds <= 60:  # 1 minute = 60 seconds
            # Warning state
            self.configure(style="Warning.TFrame")
            self.time_label.configure(foreground="black", background="orange")
        else:
            # Active state
            self.configure(style="Active.TFrame")
            self.time_label.configure(foreground="black", background="#90EE90")

    def toggle_timer(self):
        """Toggle the timer between running and paused states."""
        self.running = not self.running
        self.start_button.config(text="Stop" if self.running else "Start")
        # Update display to show correct color state
        self.update_display()
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


PRESET_AGENDA = """# Example agenda with comments
Opening remarks - 5 minutes  # Introduction and welcome
Project update - 15 minutes  # Include demo
# Break time if needed
Q&A session - 10 minutes     # Open discussion"""


def read_agenda_file(file_path):
    """Read and return the content of an agenda file."""
    try:
        with open(file_path, "r", encoding="UTF-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        return None


class AgendaTimerApp:
    """Main application class for the Agenda Timer."""

    def __init__(self, root, initial_agenda=None):
        self.root = root
        self.root.title("Agenda Timer")
        # Use system theme
        self.style = tkinter.ttk.Style()
        self.style.theme_use("clam")  # Using 'clam' as it's available across platforms
        self.timer_widgets = []
        self.initial_agenda = initial_agenda if initial_agenda else PRESET_AGENDA
        self.always_on_top = False

        self.create_widgets()
        self.setup_styles()

    def setup_styles(self):
        """Configure styles for the agenda timer application."""
        # Configure frame styles while maintaining state visibility
        self.style.configure("Inactive.TFrame")
        self.style.configure("Active.TFrame")
        self.style.configure("Warning.TFrame")
        self.style.configure("Danger.TFrame")

        # Let widgets use system theme defaults
        self.style.configure("TFrame")
        self.style.configure("TLabel")

    def toggle_text_input(self):
        """Toggle the visibility of the text input section."""
        if self.text_section.winfo_viewable():
            self.text_section.pack_forget()
            self.toggle_button.config(text="Show Text Input")
        else:
            self.text_section.pack(fill="x")
            self.toggle_button.config(text="Hide Text Input")

    def create_widgets(self):
        """Create and configure the widgets for the agenda timer application."""
        # Input area
        self.input_frame = tkinter.ttk.Frame(self.root)
        self.input_frame.pack(fill="x", padx=10, pady=5)

        # Toggle button frame
        toggle_frame = tkinter.ttk.Frame(self.input_frame)
        toggle_frame.pack(fill="x")

        self.toggle_button = tkinter.ttk.Button(
            toggle_frame, text="Hide Text Input", command=self.toggle_text_input
        )
        self.toggle_button.pack(side="left", padx=(0, 5))

        self.always_on_top = False
        self.on_top_button = tkinter.ttk.Button(
            toggle_frame, text="Stay on Top: Off", command=self.toggle_always_on_top
        )
        self.on_top_button.pack(side="left")

        # Create a container for the text input section
        self.text_section = tkinter.ttk.Frame(self.input_frame)
        self.text_section.pack(fill="x")
        # Create a frame for the load file button
        button_frame = tkinter.ttk.Frame(self.text_section)
        button_frame.pack(fill="x", anchor="w")
        tkinter.ttk.Label(
            button_frame,
            text="Enter agenda items (format: 'Description - XX minutes'):",
        ).pack(side="left")

        self.load_button = tkinter.ttk.Button(
            button_frame, text="Load File", command=self.load_file
        )
        self.load_button.pack(side="left", padx=5)

        self.text_input = tkinter.Text(self.text_section, height=10, width=50)
        self.text_input.pack(fill="x", pady=5)

        # Insert initial agenda
        self.text_input.insert("1.0", self.initial_agenda)

        # Parse button
        parse_button = tkinter.ttk.Button(
            self.text_section, text="Create Timers", command=self.parse_agenda
        )
        parse_button.pack(pady=5)

        # Timer container
        self.timer_container = tkinter.ttk.Frame(self.root)
        self.timer_container.pack(fill="both", expand=True, padx=10, pady=5)

    def toggle_always_on_top(self):
        """Toggle the window's always-on-top state."""
        self.always_on_top = not self.always_on_top
        self.root.attributes("-topmost", self.always_on_top)
        self.on_top_button.config(
            text=f"Stay on Top: {'On' if self.always_on_top else 'Off'}"
        )

    def load_file(self):
        """Open a file dialog to select and load a text file into the text input."""
        file_path = tkinter.filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="UTF-8") as file:
                    content = file.read()
                    self.text_input.delete("1.0", tkinter.END)
                    self.text_input.insert("1.0", content)
            except (IOError, OSError, UnicodeDecodeError) as e:
                tkinter.messagebox.showerror("Error", f"Failed to load file: {str(e)}")

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
            # Skip empty lines
            if not line.strip():
                continue

            # Skip comment lines starting with #
            if line.strip().startswith("#"):
                continue

            # Remove inline comments (anything after #)
            line = line.split("#")[0].strip()
            if not line:  # Skip if line was only a comment
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

    root = tkinter.Tk()
    AgendaTimerApp(root, initial_agenda)
    root.mainloop()


if __name__ == "__main__":
    main()
