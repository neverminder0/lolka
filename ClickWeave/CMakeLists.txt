cmake_minimum_required(VERSION 3.21)

project(ClickWeave VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Qt6 packages
find_package(Qt6 REQUIRED COMPONENTS Core Widgets Quick QuickControls2 Concurrent Network LinguistTools)

qt_standard_project_setup()

# Platform-specific libraries
if(WIN32)
    set(PLATFORM_LIBS user32 gdi32)
    set(PLATFORM_SOURCES 
        src/platform/windows/WindowsClickEngine.cpp
        src/platform/windows/WindowsHotkeyManager.cpp
        src/platform/windows/WindowsWindowBinder.cpp
    )
elseif(APPLE)
    find_library(COCOA_LIBRARY Cocoa)
    find_library(CARBON_LIBRARY Carbon)
    set(PLATFORM_LIBS ${COCOA_LIBRARY} ${CARBON_LIBRARY})
    set(PLATFORM_SOURCES
        src/platform/macos/MacOSClickEngine.cpp
        src/platform/macos/MacOSHotkeyManager.cpp
        src/platform/macos/MacOSWindowBinder.cpp
    )
elseif(UNIX)
    find_package(PkgConfig REQUIRED)
    pkg_check_modules(X11 REQUIRED x11 xtst xrandr)
    set(PLATFORM_LIBS ${X11_LIBRARIES})
    set(PLATFORM_SOURCES
        src/platform/linux/LinuxClickEngine.cpp
        src/platform/linux/LinuxHotkeyManager.cpp
        src/platform/linux/LinuxWindowBinder.cpp
    )
endif()

# Core sources
set(CORE_SOURCES
    src/main.cpp
    src/core/ClickEngine.cpp
    src/core/Profile.cpp
    src/core/MacroStep.cpp
    src/core/Scheduler.cpp
    src/core/PixelWatcher.cpp
    src/core/Logger.cpp
    src/core/SettingsStore.cpp
    src/ui/ProfileListModel.cpp
    src/ui/MacroStepListModel.cpp
    src/ui/ApplicationController.cpp
    ${PLATFORM_SOURCES}
)

# Headers
set(CORE_HEADERS
    src/core/ClickEngine.h
    src/core/Profile.h
    src/core/MacroStep.h
    src/core/Scheduler.h
    src/core/PixelWatcher.h
    src/core/Logger.h
    src/core/SettingsStore.h
    src/ui/ProfileListModel.h
    src/ui/MacroStepListModel.h
    src/ui/ApplicationController.h
    src/platform/HotkeyManager.h
    src/platform/WindowBinder.h
)

# QML files
set(QML_SOURCES
    ui/qml/main.qml
    ui/qml/views/HomeView.qml
    ui/qml/views/ProfileView.qml
    ui/qml/views/SettingsView.qml
    ui/qml/components/ProfileCard.qml
    ui/qml/components/MacroStepEditor.qml
    ui/qml/components/CoordinatePicker.qml
    ui/qml/components/StatusChip.qml
    ui/qml/themes/MaterialTheme.qml
    ui/qml/themes/FluentTheme.qml
)

# Resources
qt_add_resources(ClickWeave "resources"
    PREFIX "/"
    FILES
        resources/icons/app-icon.png
        resources/icons/play.svg
        resources/icons/pause.svg
        resources/icons/stop.svg
        resources/icons/settings.svg
        resources/icons/profile.svg
)

# Translation files
qt_add_translations(ClickWeave
    TS_FILES
        resources/translations/clickweave_en.ts
        resources/translations/clickweave_ru.ts
)

# Executable
qt_add_executable(ClickWeave ${CORE_SOURCES})

qt_add_qml_module(ClickWeave
    URI ClickWeave
    VERSION 1.0
    QML_FILES ${QML_SOURCES}
)

# Link libraries
target_link_libraries(ClickWeave PRIVATE
    Qt6::Core
    Qt6::Widgets
    Qt6::Quick
    Qt6::QuickControls2
    Qt6::Concurrent
    Qt6::Network
    ${PLATFORM_LIBS}
)

# Include directories
target_include_directories(ClickWeave PRIVATE
    src
    src/core
    src/ui
    src/platform
)

# Compiler definitions
target_compile_definitions(ClickWeave PRIVATE
    APP_VERSION="${PROJECT_VERSION}"
    QT_QML_DEBUG
)

# Install configuration
install(TARGETS ClickWeave
    BUNDLE DESTINATION .
    RUNTIME DESTINATION bin
)

# Testing
if(BUILD_TESTING)
    add_subdirectory(tests)
endif()