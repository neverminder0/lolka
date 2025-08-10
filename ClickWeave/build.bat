@echo off
REM ClickWeave Build Script for Windows
REM Requires Visual Studio 2019+ and Qt 6

setlocal EnableDelayedExpansion

REM Configuration
set BUILD_TYPE=Release
set BUILD_TESTS=OFF
set CLEAN_BUILD=false
set JOBS=%NUMBER_OF_PROCESSORS%
set QT_DIR=

REM Parse command line arguments
:parse_args
if "%~1"=="" goto :check_deps
if /i "%~1"=="--debug" (
    set BUILD_TYPE=Debug
    shift
    goto :parse_args
)
if /i "%~1"=="--release" (
    set BUILD_TYPE=Release
    shift
    goto :parse_args
)
if /i "%~1"=="--tests" (
    set BUILD_TESTS=ON
    shift
    goto :parse_args
)
if /i "%~1"=="--clean" (
    set CLEAN_BUILD=true
    shift
    goto :parse_args
)
if /i "%~1"=="--qt-dir" (
    set QT_DIR=%~2
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--help" (
    echo ClickWeave Build Script for Windows
    echo.
    echo Usage: %0 [OPTIONS]
    echo.
    echo Options:
    echo   --debug         Build in Debug mode
    echo   --release       Build in Release mode ^(default^)
    echo   --tests         Enable building tests
    echo   --clean         Clean build directory first
    echo   --qt-dir PATH   Specify Qt installation directory
    echo   --help          Show this help message
    exit /b 0
)
echo Unknown option: %~1
echo Use --help for usage information
exit /b 1

:check_deps
echo [INFO] Build configuration:
echo [INFO]   Build Type: %BUILD_TYPE%
echo [INFO]   Build Tests: %BUILD_TESTS%
echo [INFO]   Parallel Jobs: %JOBS%
echo [INFO]   Clean Build: %CLEAN_BUILD%

REM Check for CMake
echo [INFO] Checking build dependencies...
cmake --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] CMake not found. Please install CMake 3.21 or later.
    exit /b 1
)

REM Check for Visual Studio
if not defined VCINSTALLDIR (
    echo [INFO] Visual Studio environment not detected. Searching for VS...
    
    REM Try to find and setup Visual Studio
    if exist "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" (
        call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
    ) else if exist "C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat" (
        call "C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat"
    ) else if exist "C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat" (
        call "C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat"
    ) else if exist "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat" (
        call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
    ) else if exist "C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\Build\vcvars64.bat" (
        call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\Build\vcvars64.bat"
    ) else if exist "C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\VC\Auxiliary\Build\vcvars64.bat" (
        call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\VC\Auxiliary\Build\vcvars64.bat"
    ) else (
        echo [ERROR] Visual Studio 2019/2022 not found. Please install Visual Studio with C++ support.
        exit /b 1
    )
)

REM Check for Qt
echo [INFO] Checking Qt installation...

if "%QT_DIR%"=="" (
    REM Try to auto-detect Qt
    for %%d in (C:\Qt\6.* C:\Qt6 "C:\Program Files\Qt\6.*") do (
        if exist "%%d\msvc*\lib\cmake\Qt6\Qt6Config.cmake" (
            for /d %%v in ("%%d\msvc*") do (
                set QT_DIR=%%v
                goto :qt_found
            )
        )
    )
    
    echo [ERROR] Qt6 not found. Please specify Qt directory with --qt-dir
    echo [ERROR] Example: --qt-dir "C:\Qt\6.5.0\msvc2019_64"
    exit /b 1
)

:qt_found
if not exist "%QT_DIR%\lib\cmake\Qt6\Qt6Config.cmake" (
    echo [ERROR] Qt6 not found at: %QT_DIR%
    echo [ERROR] Please check your Qt installation
    exit /b 1
)

echo [SUCCESS] Qt6 found at: %QT_DIR%

REM Create build directory
set BUILD_DIR=build
if "%CLEAN_BUILD%"=="true" (
    if exist "%BUILD_DIR%" (
        echo [INFO] Cleaning build directory...
        rmdir /s /q "%BUILD_DIR%"
    )
)

if not exist "%BUILD_DIR%" (
    echo [INFO] Creating build directory...
    mkdir "%BUILD_DIR%"
)

cd "%BUILD_DIR%"

REM Configure CMake
echo [INFO] Configuring CMake...

set CMAKE_ARGS=-DCMAKE_BUILD_TYPE=%BUILD_TYPE% -DBUILD_TESTING=%BUILD_TESTS% -DCMAKE_PREFIX_PATH="%QT_DIR%"

cmake .. %CMAKE_ARGS%
if !errorlevel! neq 0 (
    echo [ERROR] CMake configuration failed
    exit /b 1
)

echo [SUCCESS] CMake configuration completed

REM Build
echo [INFO] Building ClickWeave...

cmake --build . --config %BUILD_TYPE% --parallel %JOBS%
if !errorlevel! neq 0 (
    echo [ERROR] Build failed
    exit /b 1
)

echo [SUCCESS] Build completed successfully!

REM Run tests if enabled
if "%BUILD_TESTS%"=="ON" (
    echo [INFO] Running tests...
    ctest --output-on-failure -C %BUILD_TYPE%
    
    if !errorlevel! equ 0 (
        echo [SUCCESS] All tests passed!
    ) else (
        echo [WARNING] Some tests failed
    )
)

REM Final information
echo [INFO] Build summary:
if exist "%BUILD_TYPE%\ClickWeave.exe" (
    echo [SUCCESS]   Executable: %CD%\%BUILD_TYPE%\ClickWeave.exe
    echo [INFO]   Run with: %BUILD_TYPE%\ClickWeave.exe
)

echo [INFO] Build completed in %CD%
pause