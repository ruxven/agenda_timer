"""Timer Widget Module"""

import tkinter
import tkinter.ttk
import tkinter.font


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
        """A widget to display and control a timer."""
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


def setup_styles(root):
    """Set up the styles used by the timer widget."""
    style = tkinter.ttk.Style(root)

    # Frame styles for different states
    style.configure("Inactive.TFrame", background="#e0e0e0")
    style.configure("Active.TFrame", background="#90EE90")
    style.configure("Warning.TFrame", background="orange")
    style.configure("Danger.TFrame", background="red")


def main():
    """Main function to run the timer widget as a standalone application."""
    root = tkinter.Tk()
    root.title("Timer Widget Test")

    # Set up the styles
    setup_styles(root)

    # Create a test timer (5 minutes)
    timer = TimerWidget(root, "Test Timer (5 minutes)", 5)
    timer.pack(padx=20, pady=20)

    # Add a quit button
    quit_button = tkinter.ttk.Button(root, text="Quit", command=root.destroy)
    quit_button.pack(pady=10)

    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()
