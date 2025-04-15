# Agenda Timer

A Python-based desktop application that helps you manage and track time during meetings or presentations. The application provides visual timers for each agenda item, with color-coded indicators to help keep your meetings on schedule.

## Features

- Create multiple timers for different agenda items
- Visual countdown for each agenda item
- Color-coded time indicators:
  - Green: Plenty of time remaining
  - Orange: Less than 1 minute remaining
  - Red: Time expired
- Start/Stop and Reset controls for each timer
- Load agenda items from a file or use the built-in text editor
- Support for custom agenda formats

## Requirements

- Python 3.x
- tkinter (usually comes with Python installation)

## Installation

1. Clone this repository or download the `agenda_timer.py` file
2. Ensure Python 3.x is installed on your system
3. No additional package installation is required as the application uses standard Python libraries

## Usage

### Running the Application

You can run the application in two ways:

1. Using the default preset agenda:
```bash
python agenda_timer.py
```

2. Loading an agenda from a file:
```bash
python agenda_timer.py --input your_agenda_file.txt
```

### Agenda Format

The agenda should follow this format:
```
Item description - X minutes
```

Example:
```
Opening remarks - 5 minutes
Project update - 15 minutes
Q&A session - 10 minutes
```

### Using the Application

1. When the application starts, you'll see a text input area with either the preset agenda or your loaded agenda file
2. Click "Create Timers" to generate timer widgets for each agenda item
3. For each timer:
   - Click "Start" to begin the countdown
   - Click "Stop" to pause the timer
   - Click "Reset" to restore the original time
4. Color indicators:
   - Green background: More than 1 minute remaining
   - Orange background: Less than 1 minute remaining
   - Red background: Time expired

### Modifying the Agenda

You can modify the agenda at any time:
1. Edit the text in the input area
2. Click "Create Timers" to update the timer widgets
3. Previous timers will be cleared and new ones will be created based on your input

## Tips

- Prepare your agenda file in advance for recurring meetings
- Keep descriptions concise but clear
- Use the color indicators to help manage your time effectively
- Reset all timers before starting a new meeting

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.