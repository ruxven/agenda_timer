"""Agenda Timer Application Module"""

import tkinter
import tkinter.ttk
import tkinter.filedialog
import re
from timer_widget import TimerWidget


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
    except UnicodeDecodeError as e:
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
        self.text_input.insert("1.0", self.initial_agenda)

        # Create button frame
        button_frame = tkinter.ttk.Frame(self.text_section)
        button_frame.pack(fill="x")

        # Add buttons
        self.update_button = tkinter.ttk.Button(
            button_frame, text="Update Timers", command=self.update_timers
        )
        self.update_button.pack(side="left", padx=5)

        # Timer container
        self.timer_container = tkinter.ttk.Frame(self.root)
        self.timer_container.pack(fill="both", expand=True, padx=10, pady=5)

        # Create initial timers
        self.update_timers()

    def toggle_always_on_top(self):
        """Toggle the always-on-top state of the window."""
        self.always_on_top = not self.always_on_top
        self.root.attributes("-topmost", self.always_on_top)
        self.on_top_button.config(
            text=f"Stay on Top: {'On' if self.always_on_top else 'Off'}"
        )

    def load_file(self):
        """Load agenda items from a file."""
        file_path = tkinter.filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            content = read_agenda_file(file_path)
            if content is not None:
                self.text_input.delete("1.0", "end")
                self.text_input.insert("1.0", content)
                self.update_timers()

    def parse_agenda_text(self):
        """Parse the agenda text and return a list of (description, minutes) tuples."""
        text = self.text_input.get("1.0", "end").strip()
        items = []

        for line in text.split("\n"):
            # Skip empty lines and comments
            if not line.strip() or line.strip().startswith("#"):
                continue

            # Remove inline comments
            line = line.split("#")[0].strip()

            # Try to match "Description - X minutes" pattern
            match = re.match(r"(.*?)\s*-\s*(\d+)\s*(?:minute|minutes|min|m)?", line)
            if match:
                description = match.group(1).strip()
                minutes = int(match.group(2))
                items.append((description, minutes))

        return items

    def update_timers(self):
        """Update the timer widgets based on the current agenda text."""
        # Clear existing timers
        for widget in self.timer_widgets:
            widget.destroy()
        self.timer_widgets.clear()

        # Create new timers
        for description, minutes in self.parse_agenda_text():
            timer = TimerWidget(self.timer_container, description, minutes)
            timer.pack(fill="x", pady=2)
            self.timer_widgets.append(timer)
