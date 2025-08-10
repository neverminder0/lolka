# ClickWeave - Cross-Platform Auto-Clicker

A modern, productivity-focused auto-clicker built with Qt 6 and C++20. Designed for UI testing, form automation, and productivity tasks.

![ClickWeave Screenshot](screenshots/main-window.png)

## Features

### Core Functionality
- **Cross-platform support**: Windows 10/11, macOS 13+, Linux (X11)
- **Global hotkeys**: F8 (Start/Stop), F7 (Pause), Esc (Emergency Stop)
- **Multiple click modes**: Single, Double, Hold clicks
- **Mouse button support**: Left, Right, Middle, Scroll wheel
- **Keyboard automation**: Key press sequences
- **Precise timing**: High-precision timers with jitter randomization

### Advanced Features
- **Click Profiles**: Unlimited profiles with JSON import/export
- **Macro Recording**: Record and edit complex sequences
- **Pixel Triggers**: Click when specific colors appear on screen
- **Window Targeting**: Bind to specific windows by title/process
- **Scheduler**: CRON-like scheduling for automated runs
- **Safety Features**: Failsafe stops, corner detection, single-instance lock

### Modern UI
- **Material Design**: Clean, modern interface with light/dark themes
- **Responsive Layout**: Adaptive design for different screen sizes
- **Real-time Status**: Live click counters and status indicators
- **Coordinate Picker**: Visual coordinate selection tool
- **Internationalization**: English and Russian language support

## Installation

### Windows (Recommended)
1. Download the latest release from [Releases](../../releases)
2. Extract the archive
3. Run `ClickWeave.exe`

### Building from Source

#### Prerequisites
- Qt 6.5 or later
- CMake 3.21 or later
- C++20 compatible compiler (MSVC 2019+, GCC 10+, Clang 12+)

#### Windows
```bash
# Install Qt 6 and Visual Studio 2019+
mkdir build && cd build
cmake .. -DCMAKE_PREFIX_PATH="C:/Qt/6.5.0/msvc2019_64"
cmake --build . --config Release
```

#### Linux
```bash
# Install dependencies
sudo apt-get install qt6-base-dev qt6-declarative-dev qt6-tools-dev \
                     libx11-dev libxtst-dev libxrandr-dev

mkdir build && cd build
cmake ..
make -j$(nproc)
```

#### macOS
```bash
# Install Qt 6 via Homebrew
brew install qt@6

mkdir build && cd build
cmake .. -DCMAKE_PREFIX_PATH="/opt/homebrew/opt/qt@6"
make -j$(sysctl -n hw.ncpu)
```

## Usage

### Quick Start
1. Launch ClickWeave
2. Create a new profile or load a demo profile
3. Configure click positions and timing
4. Press F8 to start/stop clicking
5. Use F7 to pause/resume, Esc for emergency stop

### Demo Profiles
Two demo profiles are included:

**Form Test**: Clicks a button every 2 seconds, 20 times
- Ideal for testing form submissions or button interactions
- Uses 10% timing jitter for natural clicking

**Pixel Trigger**: Clicks when a green color appears at specific coordinates
- Demonstrates conditional clicking based on screen content
- Includes keyboard automation (Space key press)

### Safety Features
- **Emergency Stop**: Rapid mouse movement to screen corner stops all activity
- **Global Hotkeys**: Work even when ClickWeave is not focused
- **Single Instance**: Prevents multiple instances from running
- **Privilege Escalation**: Only requests elevated privileges when needed

## Ethical Use

ClickWeave is designed for legitimate productivity and testing purposes:

✅ **Intended Uses:**
- UI testing and automation
- Form filling and data entry
- Productivity workflows
- Browser automation for legitimate tasks
- Office application automation

❌ **Not Intended For:**
- Bypassing game anti-cheat systems
- Automating competitive gaming
- Circumventing security measures
- Any malicious activities

## Configuration

### Global Hotkeys
- `F8`: Start/Stop clicking
- `F7`: Pause/Resume (only when running)
- `Esc`: Emergency stop (works globally)

### Profile Settings
- **Interval**: Time between clicks (ms/sec/min)
- **Jitter**: Randomization percentage (0-100%)
- **Repeat Count**: Number of repetitions (0 = infinite)
- **Duration Limit**: Maximum runtime in milliseconds
- **Window Binding**: Target specific windows or processes

### Data Storage
- **Windows**: `%APPDATA%/ClickWeave/`
- **macOS**: `~/Library/Application Support/ClickWeave/`
- **Linux**: `~/.local/share/ClickWeave/`

## Architecture

### Core Components
- **ClickEngine**: Platform-specific click implementation
- **Profile/MacroStep**: Configuration and sequence management
- **HotkeyManager**: Global keyboard shortcut handling
- **WindowBinder**: Window targeting and coordinate conversion
- **PixelWatcher**: Screen color detection
- **Scheduler**: CRON-like task scheduling

### Platform Abstraction
- **Windows**: Uses SendInput API for mouse/keyboard events
- **Linux**: Uses X11 XTest extension
- **macOS**: Uses Core Graphics and Carbon events

## Development

### Project Structure
```
ClickWeave/
├── src/
│   ├── core/           # Core business logic
│   ├── ui/             # Qt/QML UI components
│   ├── platform/       # Platform-specific implementations
│   └── main.cpp        # Application entry point
├── ui/qml/             # QML user interface
├── resources/          # Icons, translations, assets
├── tests/              # Unit tests
├── profiles/           # Demo profiles
└── CMakeLists.txt      # Build configuration
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Follow the existing code style
4. Add tests for new functionality
5. Submit a pull request

### Testing
```bash
# Build with tests enabled
cmake .. -DBUILD_TESTING=ON
make -j$(nproc)

# Run tests
ctest --output-on-failure
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Qt Framework for cross-platform GUI development
- Material Design for UI/UX inspiration
- Contributors and beta testers

## Support

- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)
- **Documentation**: [Wiki](../../wiki)

---

**Version**: 1.0.0  
**Build Date**: 2024-01-01  
**Qt Version**: 6.5+  
**Platforms**: Windows 10/11, macOS 13+, Linux (X11)