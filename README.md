
# Peppy G-TEC: Keep Teams Status Green!

## Overview

**Peppy G-TEC** ("AlwaysGreen") is a Python package that prevents system inactivity by simulating mouse movement and clicks during configured working hours. It ensures that status indicators (such as Microsoft Teams) remain green/active and do not fall back to orange or away during specified working periods.

A click is required — not just a mouse move — because Teams only transitions from orange back to green when a click event is detected.

This script is helpful for:
- Keeping Teams status green during working hours.
- Preventing auto-logout or screensaver activation while you are briefly away.

---

## Key Features

1. **Activity Detection**:
   - Monitors mouse and keyboard actions using the `pynput` library.

2. **Timeout-Based Activity**:
   - Simulates activity (move + click) after a user-defined period of inactivity.

3. **Working Periods per Day**:
   - Define time windows per day of the week during which activity is enforced.
   - Outside working hours the script runs but does not simulate any input.

4. **Modern Output**:
   - Optional colored and emoji-based status outputs.

5. **Customizable Settings**:
   - Timeout duration, logo display, status and working period visibility.

6. **Real-Time Feedback**:
   - Outputs activity status in real-time with optional colored text.

7. **Keyboard Interrupt Handling**: Graceful termination with `CTRL-C`.

---

## How It Works

1. **Initialization**:
   - The script initializes with configurable parameters: timeout, working periods, colored output, and logo display.

2. **Event Listeners**:
   - Monitors mouse and keyboard events to detect user activity and reset the inactivity timer.

3. **Mouse Movement + Click**:
   - Moves the mouse to `(0, 0)` and simulates a left-click to bring Teams back to green.
   - If the mouse is already at `(0, 0)`, moves it by a fixed distance instead.

4. **Working Period Check**:
   - Re-evaluated every second and on every user event so hour boundaries are respected automatically.

5. **Continuous Monitoring**:
   - Runs indefinitely, alternating between monitoring inactivity and simulating activity.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Install the Package

```bash
# Clone or download the repository
git clone <repository-url>
cd GT

# Install in development mode (recommended for development)
pip install -e .

# Or install normally
pip install .
```

Once installed, you can run the CLI from anywhere:

```bash
peppy-gtec --help
```

---

## Usage

Run the CLI tool from the command line:

```bash
peppy-gtec [OPTIONS]
```

### Command-Line Arguments

|          Argument          | Default  | Description                                                                                                                                                      |
|:--------------------------:|:--------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| `--time`                   | `5`      | Timeout period in seconds before inactivity action is taken.                                                                                                     |
| `--classic`                | Disabled | Enable classic (non-colored) output mode.                                                                                                                        |
| `--no-logo`                | Disabled | Disable the display of the logo.                                                                                                                                 |
| `--no-instructions`        | Disabled | Disable the display of the instructions.                                                                                                                         |
| `--no-working-period`      | Disabled | Disable the display of working periods at startup.                                                                                                               |
| `--no-status`              | Disabled | Disable the real-time activity status line.                                                                                                                      |
| `--working-period`         | None     | Add working periods in the format `DAY:HH:MM:SS-HH:MM:SS`. Multiple periods separated by space. DAY must be one of: `MON TUE WED THU FRI SAT SUN`.               |
| `--force-enforce`          | Disabled | Start in forced ENFORCED mode (ignores schedule until cancelled).                                                                                                |
| `--force-release`          | Disabled | Start in forced RELEASED mode (ignores schedule until cancelled).                                                                                                |

### On-the-Fly Force Controls

While running, you can switch behavior at any time using hotkeys:

- `CTRL+ALT+E` -> Force ENFORCED
- `CTRL+ALT+R` -> Force RELEASED
- `CTRL+ALT+C` -> Cancel force mode (return to working-period schedule)

---

## Default Working Periods

When `--working-period` is not specified, the following defaults are used:

| Day       | Start    | End      |
|:---------:|:--------:|:--------:|
| Monday    | 08:30:00 | 17:30:00 |
| Tuesday   | 08:30:00 | 17:30:00 |
| Wednesday | 08:30:00 | 17:30:00 |
| Thursday  | 08:30:00 | 17:30:00 |
| Friday    | 08:30:00 | 17:30:00 |
| Saturday  | —        | —        |
| Sunday    | —        | —        |

---

## Examples

### Basic Usage

Run with default settings (Mon–Fri 08:30–17:30, 5-second timeout):

```bash
peppy-gtec
```

Run with a 60-second timeout:

```bash
peppy-gtec --time 60
```

Run without colored output:

```bash
peppy-gtec --time 60 --classic
```

Run without displaying working periods or the logo:

```bash
peppy-gtec --no-logo --no-working-period
```

Run with custom working periods:

```bash
peppy-gtec --working-period MON:08:30:00-17:30:00 TUE:08:30:00-17:30:00 WED:08:30:00-17:30:00 THU:08:30:00-17:30:00 FRI:08:30:00-17:30:00
```

Start in forced ENFORCED mode:

```bash
peppy-gtec --force-enforce
```

Start in forced RELEASED mode:

```bash
peppy-gtec --force-release
```

Run with different hours on different days:

```bash
peppy-gtec --working-period MON:09:00:00-18:00:00 FRI:09:00:00-14:00:00
```

---

## Using as a Python Library

You can also import and use `AlwaysGreen` as a library in your own Python code:

```python
from peppy_gtec import AlwaysGreen

working_periods = {
    'MON': [('08:30:00', '17:30:00')],
    'TUE': [('08:30:00', '17:30:00')],
    'WED': [('08:30:00', '17:30:00')],
    'THU': [('08:30:00', '17:30:00')],
    'FRI': [('08:30:00', '17:30:00')],
    'SAT': [],
    'SUN': [],
}

aw = AlwaysGreen(
    timeout_period=60,
    working_periods=working_periods,
    modern_output=True,
    show_status=True,
)

try:
    aw.run()
except KeyboardInterrupt:
    print("\nStopped")
```

---

## Development

### Setup Development Environment

To set up a development environment:

```bash
# Clone the repository
git clone <repository-url>
cd GT

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Linux/macOS

# Install development dependencies
pip install -r requirements-dev.txt
```

### Code Quality Tools

Run these tools to maintain code quality:

```bash
# Format code with black
black peppy_gtec/

# Sort imports with isort
isort peppy_gtec/

# Lint with flake8
flake8 peppy_gtec/

# Type checking with mypy
mypy peppy_gtec/

# Run tests (if available)
pytest
```

### Building and Distributing

To build and distribute the package:

```bash
# Install build tools
pip install build

# Build wheel and source distribution
python -m build

# This creates:
# - dist/Peppy\ G-TEC-1.0.0-py3-none-any.whl
# - dist/Peppy\ G-TEC-1.0.0.tar.gz
```

---

## Output Example

The script displays activity status dynamically:

**Default Mode (colored)**
```
| ENFORCED | Inactive in     5s | Status:🟡 |
```

**During non-working hours**
```
| RELEASED | Inactive in     5s | Status:🟢 |
```

**Classic Mode**
```
| ENFORCED | Inactive in     5s | #INACTIVE |
```

---

## Dependencies

The package automatically installs required dependencies when you run `pip install .`

- **pynput** (>=1.7.6): A library for controlling and monitoring mouse and keyboard events.
  - See [pynput on PyPI](https://pypi.org/project/pynput/)

### Development Dependencies

For development and testing, optional tools are listed in `requirements-dev.txt`:

```bash
pip install -r requirements-dev.txt
```

---

## Project Structure

```
peppy_gtec/
├── __init__.py              # Package initialization
├── core.py                  # Core AlwaysGreen class
└── cli.py                   # Command-line interface
```

---

## References

1. [pynput library on PyPI](https://pypi.org/project/pynput/)
2. [Python Packaging Guide](https://packaging.python.org/)
3. [How to Make a Python Auto Clicker - GeeksforGeeks](https://www.geeksforgeeks.org/how-to-make-a-python-auto-clicker/)
4. [ASCII Art Generator - asciiart.eu](https://www.asciiart.eu/text-to-ascii-art)
5. [Print Colors in Python Terminal - GeeksforGeeks](https://www.geeksforgeeks.org/print-colors-python-terminal/)

---

## Troubleshooting

### Command not found: peppy-gtec
Make sure you've installed the package:
```bash
pip install -e .
```

### ModuleNotFoundError: No module named 'pynput'
Install the dependencies:
```bash
pip install -r requirements.txt
```

### Permissions denied on Windows
Run your terminal as Administrator if mouse movement is being blocked by system policies.

---

## License

This project is free to use and modify. Contributions are welcome!

---

## Contributing

Feel free to fork, modify, and improve this project. To contribute:

1. Make your changes in a new branch
2. Test thoroughly
3. Submit a pull request

---

## Changelog

### v1.0.0 (Current)
- Restructured as a Python package with CLI interface
- Added `pyproject.toml` for modern Python packaging
- Created CLI entry point: `peppy-gtec`
- Improved documentation and examples
- Added development tools configuration

