# ClickWeave-Py

A cross-platform Python auto-clicker and macro automation tool with a modern CustomTkinter UI. Designed for productivity and UI testing purposes.

![ClickWeave-Py Logo](assets/screenshot.png)

## 🚀 Features

### Core Automation
- **Global Hotkeys**: Start/Stop (F8), Pause/Resume (F7), Emergency Stop (Esc)
- **Unlimited Profiles**: Save and manage unlimited click profiles as JSON files
- **Multiple Input Modes**: Left/Right/Middle click, double click, hold actions
- **Key Press Support**: Automated keyboard inputs with modifier key combinations
- **Macro Sequences**: Complex automation with clicks, moves, delays, and key presses

### Advanced Timing
- **Flexible Intervals**: Configure timing in milliseconds, seconds, or minutes
- **Natural Jitter**: Add ±X% randomization for human-like behavior
- **Execution Limits**: Set maximum clicks or duration limits
- **Precise Timing**: High-resolution timing with threading for accuracy

### Smart Triggers
- **Manual Control**: Start/stop via UI or global hotkeys
- **Scheduled Automation**: Start at specific date/time with CRON-like repeats
- **Pixel Color Triggers**: Trigger automation when screen colors match conditions
- **Coordinate Picker**: Visual "eyedropper" tool with live XY and RGB preview

### Macro Recording & Editing
- **Record Sessions**: Capture mouse movements, clicks, and keyboard inputs
- **Visual Editor**: Table-based step editor with reorder, duplicate, and loop options
- **Step Types**: Support for clicks, moves, delays, key presses, and scrolling
- **Loop Control**: Repeat individual steps or entire sequences

### Safety & Reliability
- **Failsafe Protection**: Emergency stop by moving mouse to screen corner
- **Single Instance**: Prevents multiple app instances from running
- **Robust Error Handling**: Comprehensive logging and error recovery
- **Safe Automation**: Designed for productivity, not for bypassing security systems

### Analytics & Logging
- **Execution History**: Track all automation runs with detailed statistics
- **Performance Metrics**: Monitor clicks, duration, and average intervals
- **CSV Export**: Export logs for analysis in spreadsheet applications
- **Real-time Statistics**: Live monitoring of automation progress

### Modern UI & Customization
- **Dark/Light Themes**: Modern CustomTkinter interface with theme switching
- **Internationalization**: Support for English and Russian languages
- **Responsive Design**: Adaptive layout that works on different screen sizes
- **Accent Colors**: Customizable color themes

## 🛠️ Tech Stack

- **UI Framework**: CustomTkinter for modern, native-looking interface
- **Automation**: PyAutoGUI and pynput for cross-platform mouse/keyboard control
- **Global Hotkeys**: keyboard library for system-wide hotkey registration
- **Screen Capture**: MSS for fast pixel color detection and screenshots
- **Scheduling**: APScheduler for time-based automation triggers
- **Data Models**: Pydantic for robust data validation and serialization
- **Storage**: JSON for profiles, CSV for logs
- **Packaging**: PyInstaller for standalone executable creation

## 📋 Requirements

- **Python**: 3.10 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 100MB RAM minimum
- **Storage**: 50MB disk space
- **Permissions**: Access to mouse/keyboard input (may require admin rights on some systems)

## 🚀 Installation

### Option 1: From Source

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ClickWeave-Py.git
   cd ClickWeave-Py
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

### Option 2: Pre-built Executable

1. Download the latest release for your platform from the [Releases](https://github.com/yourusername/ClickWeave-Py/releases) page
2. Extract the archive
3. Run `ClickWeave-Py.exe` (Windows) or the appropriate executable for your platform

### Option 3: Build Your Own Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --icon=assets/icon.ico main.py

# Find executable in dist/ folder
```

## 🎯 Quick Start Guide

### Creating Your First Profile

1. **Launch ClickWeave-Py** and click "New Profile"
2. **Set Basic Information**:
   - Name: "Website Auto-refresh"
   - Description: "Refreshes web page every 30 seconds"

3. **Configure Click Settings**:
   - Click Type: Left Click
   - Use "Pick Position" to select the refresh button location

4. **Set Timing**:
   - Interval: 30000 ms (30 seconds)
   - Jitter: 5% (for natural variation)

5. **Save and Start**: Save the profile and click "Start" to begin automation

### Using Global Hotkeys

- **F8**: Start/Stop the last active profile
- **F7**: Pause/Resume current automation
- **Esc**: Emergency stop (immediate termination)

### Creating Macro Sequences

1. Create a new profile and switch to the "Steps/Macro" tab
2. Add steps using the step editor:
   - **Click Step**: Click at specific coordinates
   - **Move Step**: Move mouse without clicking
   - **Delay Step**: Wait for specified time
   - **Key Step**: Press keyboard keys with modifiers
   - **Scroll Step**: Scroll up or down

3. Reorder steps by dragging, set loop counts, and test individual steps

## 📖 User Guide

### Profile Management

#### Creating Profiles
- Click "New Profile" in the main window
- Fill in the profile details in the editor
- Configure automation settings
- Save to create the profile

#### Profile Organization
- Profiles are stored as JSON files in `app/data/profiles/`
- Import/export profiles for sharing or backup
- Duplicate profiles to create variations
- Delete unused profiles to keep your workspace clean

### Automation Types

#### Simple Clicking
Best for repetitive clicking tasks:
- Set target coordinates
- Choose click type (left, right, middle, double, hold)
- Configure timing and limits
- Add jitter for natural behavior

#### Complex Macros
For multi-step automation:
- Record actions or manually create steps
- Combine clicks, movements, and keyboard input
- Use delays between steps
- Loop individual steps or entire sequences

#### Triggered Automation
For conditional automation:
- **Pixel Triggers**: Start when screen color changes
- **Scheduled Triggers**: Run at specific times
- **Manual Triggers**: Start via UI or hotkeys

### Safety Features

#### Failsafe Protection
- Move mouse to any screen corner for emergency stop
- Configurable in Settings > Safety
- Works even when automation is running

#### Single Instance Lock
- Prevents multiple app instances
- Ensures clean resource usage
- Configurable in application settings

### Settings & Customization

#### Appearance
- **Theme**: Dark, Light, or System
- **Language**: English or Russian
- **Accent Color**: Customizable UI colors

#### Hotkeys
- Configure global hotkey combinations
- Test hotkeys before applying
- Disable if conflicts with other applications

#### Safety Options
- Enable/disable failsafe corner detection
- Set failsafe corner location
- Configure emergency stop behavior

## 🔧 Advanced Usage

### Pixel Color Triggers

1. **Set Target Coordinates**: Use the coordinate picker to select the pixel to monitor
2. **Capture Color**: The tool automatically captures the current color
3. **Set Condition**:
   - **Exact**: Trigger when color matches exactly (within tolerance)
   - **Similar**: Trigger when color is similar (adjustable tolerance)
   - **Changed**: Trigger when color changes from initial value
4. **Configure Monitoring**: Set check interval for optimal performance

### Scheduled Automation

#### Simple Scheduling
- Set start date and time
- Optionally set repeat interval (e.g., every 30 minutes)
- Set end date/time to stop repeating

#### CRON Expressions
For complex scheduling, use CRON expressions:
- `0 9 * * 1-5`: Every weekday at 9:00 AM
- `*/15 * * * *`: Every 15 minutes
- `0 12 1 * *`: First day of every month at noon

### Macro Recording

1. **Start Recording**: Click "Record" in the macro editor
2. **Perform Actions**: Execute the actions you want to automate
3. **Stop Recording**: Click "Stop" when finished
4. **Edit Steps**: Modify timing, add loops, or remove unwanted steps
5. **Test Macro**: Run the macro to verify correct operation

### Log Analysis

#### Execution History
- View all automation runs in the Logs tab
- Filter by profile, date, or execution status
- Export to CSV for detailed analysis

#### Performance Metrics
- Monitor average execution times
- Track click accuracy and timing consistency
- Identify optimal settings for your use cases

## 🏗️ Project Structure

```
ClickWeave-Py/
├── app/
│   ├── core/                  # Core automation engines
│   │   ├── application.py     # Main application controller
│   │   ├── click_engine.py    # Mouse clicking automation
│   │   ├── macro_engine.py    # Macro sequence execution
│   │   ├── hotkey_manager.py  # Global hotkey handling
│   │   ├── pixel_watcher.py   # Pixel color monitoring
│   │   └── scheduler.py       # Time-based triggers
│   ├── models/                # Data models
│   │   └── models.py          # Pydantic data models
│   ├── ui/                    # User interface
│   │   ├── main_window.py     # Main application window
│   │   ├── widgets/           # Reusable UI components
│   │   └── windows/           # Dialog windows
│   └── data/                  # Application data
│       ├── profiles/          # Profile JSON files
│       ├── logs/              # Execution logs (CSV)
│       └── settings.json      # Application settings
├── tests/                     # Unit tests
├── assets/                    # Icons and images
├── requirements.txt           # Python dependencies
├── main.py                   # Application entry point
└── pyinstaller.spec          # Build configuration
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=app

# Run specific test file
python -m pytest tests/test_click_engine.py
```

### Test Coverage

The test suite covers:
- ✅ Core automation engines
- ✅ Data model validation
- ✅ Timing and jitter calculations
- ✅ Profile serialization/deserialization
- ✅ Error handling and edge cases

## 🔒 Security & Safety

### Designed for Productivity
ClickWeave-Py is designed for legitimate productivity and testing purposes:
- ✅ Office automation and data entry
- ✅ UI testing and quality assurance
- ✅ Repetitive task automation
- ✅ Accessibility assistance

### Not for Gaming or Exploits
This tool should NOT be used for:
- ❌ Game automation or botting
- ❌ Bypassing anti-cheat systems
- ❌ Exploiting online services
- ❌ Automated clicking on ads or revenue systems

### Privacy & Data
- No data is sent to external servers
- All profiles and logs are stored locally
- No telemetry or usage tracking
- Open source code for transparency

## 🚨 Troubleshooting

### Common Issues

#### "Permission Denied" Errors
**Problem**: Application can't control mouse/keyboard
**Solution**: 
- Run as administrator (Windows)
- Grant accessibility permissions (macOS)
- Install xdotool (Linux): `sudo apt install xdotool`

#### Global Hotkeys Not Working
**Problem**: Hotkeys don't respond
**Solution**:
- Check for conflicting applications
- Try different key combinations
- Run with elevated privileges
- Disable other hotkey software temporarily

#### High CPU Usage
**Problem**: Application uses too much CPU
**Solution**:
- Increase automation intervals
- Reduce pixel monitoring frequency
- Close unnecessary background applications
- Lower jitter percentages

#### Clicking Accuracy Issues
**Problem**: Clicks miss target locations
**Solution**:
- Recalibrate coordinates using "Pick Position"
- Check for display scaling issues
- Ensure target window is in focus
- Test with slower automation speeds

### Getting Help

1. **Check the Wiki**: Detailed guides and FAQs
2. **Search Issues**: Look for similar problems in GitHub Issues
3. **Create Issue**: Report bugs with detailed information
4. **Discussion Forum**: Ask questions and share tips

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/ClickWeave-Py.git
cd ClickWeave-Py

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
python -m pytest

# Run application in development mode
python main.py
```

### Code Standards

- **Type Hints**: All functions must have type hints
- **Docstrings**: Comprehensive documentation for all public methods
- **Testing**: Unit tests for all core functionality
- **Formatting**: Code formatted with Black and isort
- **Linting**: Clean Pylint and Flake8 results

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CustomTkinter**: Modern UI framework by Tom Schimansky
- **PyAutoGUI**: Cross-platform automation by Al Sweigart
- **pynput**: Input device control library
- **APScheduler**: Advanced scheduling capabilities
- **Pydantic**: Robust data validation and settings management

## 📊 Project Statistics

- **Lines of Code**: ~3,000
- **Test Coverage**: 85%+
- **Supported Platforms**: Windows, macOS, Linux
- **Python Version**: 3.10+
- **Dependencies**: 11 core packages

## 🗺️ Roadmap

### Version 1.1.0
- [ ] Enhanced macro recording with image recognition
- [ ] Plugin system for custom automation types
- [ ] Cloud profile synchronization
- [ ] Mobile companion app for remote control

### Version 1.2.0
- [ ] Machine learning for adaptive timing
- [ ] OCR-based automation triggers
- [ ] Advanced scripting with Python integration
- [ ] Team collaboration features

---

**⚠️ Disclaimer**: Use ClickWeave-Py responsibly and in accordance with the terms of service of the applications and websites you interact with. The developers are not responsible for any misuse of this software.

**💝 Support**: If you find ClickWeave-Py useful, please consider starring the repository and sharing it with others who might benefit from automation tools!