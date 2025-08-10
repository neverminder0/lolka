#!/bin/bash

# ClickWeave Build Script
# Supports Linux and macOS

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect OS
OS=""
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    print_error "Unsupported operating system: $OSTYPE"
    exit 1
fi

print_status "Detected OS: $OS"

# Configuration
BUILD_TYPE="Release"
BUILD_TESTS="OFF"
CLEAN_BUILD="false"
JOBS=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo "4")

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --debug)
            BUILD_TYPE="Debug"
            shift
            ;;
        --release)
            BUILD_TYPE="Release"
            shift
            ;;
        --tests)
            BUILD_TESTS="ON"
            shift
            ;;
        --clean)
            CLEAN_BUILD="true"
            shift
            ;;
        --jobs)
            JOBS="$2"
            shift 2
            ;;
        --help)
            echo "ClickWeave Build Script"
            echo ""
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --debug         Build in Debug mode"
            echo "  --release       Build in Release mode (default)"
            echo "  --tests         Enable building tests"
            echo "  --clean         Clean build directory first"
            echo "  --jobs N        Use N parallel jobs (default: auto-detect)"
            echo "  --help          Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

print_status "Build configuration:"
print_status "  Build Type: $BUILD_TYPE"
print_status "  Build Tests: $BUILD_TESTS"
print_status "  Parallel Jobs: $JOBS"
print_status "  Clean Build: $CLEAN_BUILD"

# Check for required tools
print_status "Checking build dependencies..."

if ! command -v cmake &> /dev/null; then
    print_error "CMake not found. Please install CMake 3.21 or later."
    exit 1
fi

if ! command -v make &> /dev/null && ! command -v ninja &> /dev/null; then
    print_error "Neither make nor ninja found. Please install a build system."
    exit 1
fi

# Check Qt installation
print_status "Checking Qt installation..."

QT_DIR=""
if [[ "$OS" == "linux" ]]; then
    # Try to find Qt6 on Linux
    for qt_path in /usr/lib/x86_64-linux-gnu/cmake/Qt6 /usr/lib/cmake/Qt6 /opt/qt6/lib/cmake/Qt6; do
        if [[ -d "$qt_path" ]]; then
            QT_DIR="$qt_path"
            break
        fi
    done
    
    if [[ -z "$QT_DIR" ]]; then
        print_warning "Qt6 not found in standard locations. Trying pkg-config..."
        if command -v pkg-config &> /dev/null && pkg-config --exists Qt6Core; then
            print_success "Qt6 found via pkg-config"
        else
            print_error "Qt6 not found. Please install qt6-base-dev qt6-declarative-dev"
            echo "Ubuntu/Debian: sudo apt-get install qt6-base-dev qt6-declarative-dev qt6-tools-dev"
            echo "Fedora: sudo dnf install qt6-qtbase-devel qt6-qtdeclarative-devel"
            exit 1
        fi
    else
        print_success "Qt6 found at: $QT_DIR"
    fi
elif [[ "$OS" == "macos" ]]; then
    # Try to find Qt6 on macOS
    for qt_path in /opt/homebrew/opt/qt@6/lib/cmake/Qt6 /usr/local/opt/qt@6/lib/cmake/Qt6; do
        if [[ -d "$qt_path" ]]; then
            QT_DIR="$qt_path"
            break
        fi
    done
    
    if [[ -z "$QT_DIR" ]]; then
        print_error "Qt6 not found. Please install Qt6 via Homebrew:"
        echo "brew install qt@6"
        exit 1
    else
        print_success "Qt6 found at: $QT_DIR"
    fi
fi

# Create build directory
BUILD_DIR="build"
if [[ "$CLEAN_BUILD" == "true" ]] && [[ -d "$BUILD_DIR" ]]; then
    print_status "Cleaning build directory..."
    rm -rf "$BUILD_DIR"
fi

if [[ ! -d "$BUILD_DIR" ]]; then
    print_status "Creating build directory..."
    mkdir -p "$BUILD_DIR"
fi

cd "$BUILD_DIR"

# Configure CMake
print_status "Configuring CMake..."

CMAKE_ARGS=(
    -DCMAKE_BUILD_TYPE="$BUILD_TYPE"
    -DBUILD_TESTING="$BUILD_TESTS"
)

if [[ -n "$QT_DIR" ]]; then
    CMAKE_ARGS+=(-DCMAKE_PREFIX_PATH="$QT_DIR")
fi

if command -v ninja &> /dev/null; then
    CMAKE_ARGS+=(-G Ninja)
    BUILD_TOOL="ninja"
else
    BUILD_TOOL="make"
fi

cmake .. "${CMAKE_ARGS[@]}"

if [[ $? -ne 0 ]]; then
    print_error "CMake configuration failed"
    exit 1
fi

print_success "CMake configuration completed"

# Build
print_status "Building ClickWeave..."

if [[ "$BUILD_TOOL" == "ninja" ]]; then
    ninja -j "$JOBS"
else
    make -j "$JOBS"
fi

if [[ $? -ne 0 ]]; then
    print_error "Build failed"
    exit 1
fi

print_success "Build completed successfully!"

# Run tests if enabled
if [[ "$BUILD_TESTS" == "ON" ]]; then
    print_status "Running tests..."
    ctest --output-on-failure
    
    if [[ $? -eq 0 ]]; then
        print_success "All tests passed!"
    else
        print_warning "Some tests failed"
    fi
fi

# Final information
print_status "Build summary:"
if [[ "$OS" == "linux" ]]; then
    if [[ -f "ClickWeave" ]]; then
        print_success "  Executable: $(pwd)/ClickWeave"
        print_status "  Run with: ./ClickWeave"
    fi
elif [[ "$OS" == "macos" ]]; then
    if [[ -d "ClickWeave.app" ]]; then
        print_success "  App Bundle: $(pwd)/ClickWeave.app"
        print_status "  Run with: open ClickWeave.app"
    fi
fi

print_status "Build completed in $(pwd)"