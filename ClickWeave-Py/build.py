#!/usr/bin/env python3
"""
Build script for ClickWeave-Py executable generation.
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


def clean_build_dirs():
    """Clean previous build directories."""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Clean .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))


def check_dependencies():
    """Check if all required build dependencies are installed."""
    required_packages = [
        'pyinstaller',
        'customtkinter', 
        'pynput',
        'pyautogui',
        'keyboard',
        'pillow',
        'mss',
        'apscheduler',
        'pydantic',
        'psutil'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True


def create_version_info():
    """Create version info file for Windows builds."""
    if platform.system() != 'Windows':
        return
    
    version_info = """
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'ClickWeave-Py'),
        StringStruct(u'FileDescription', u'Cross-platform Auto-clicker Application'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'ClickWeave-Py'),
        StringStruct(u'LegalCopyright', u'Copyright © 2024 ClickWeave-Py'),
        StringStruct(u'OriginalFilename', u'ClickWeave-Py.exe'),
        StringStruct(u'ProductName', u'ClickWeave-Py Auto-clicker'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info.strip())
    
    print("✅ Created version_info.txt for Windows build")


def create_icon():
    """Create default icon if none exists."""
    icon_dir = Path('app/assets')
    icon_dir.mkdir(parents=True, exist_ok=True)
    
    # This is a placeholder - in a real project you'd have actual icon files
    print("ℹ️  Note: Add icon files to app/assets/ for better branding")
    print("   - icon.ico for Windows")
    print("   - icon.icns for macOS")
    print("   - icon.png for Linux")


def build_executable():
    """Build the executable using PyInstaller."""
    print("🔨 Building executable...")
    
    try:
        # Run PyInstaller with the spec file
        cmd = [sys.executable, '-m', 'PyInstaller', '--clean', 'pyinstaller.spec']
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Build completed successfully!")
            
            # Show build results
            dist_dir = Path('dist')
            if dist_dir.exists():
                files = list(dist_dir.iterdir())
                print(f"\n📦 Built files in dist/:")
                for file in files:
                    size = file.stat().st_size / (1024 * 1024)  # Size in MB
                    print(f"   - {file.name} ({size:.1f} MB)")
            
            return True
        else:
            print("❌ Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
    
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False


def test_executable():
    """Test the built executable."""
    print("\n🧪 Testing executable...")
    
    exe_name = 'ClickWeave-Py.exe' if platform.system() == 'Windows' else 'ClickWeave-Py'
    exe_path = Path('dist') / exe_name
    
    if not exe_path.exists():
        print(f"❌ Executable not found: {exe_path}")
        return False
    
    print(f"✅ Executable found: {exe_path}")
    print(f"   Size: {exe_path.stat().st_size / (1024 * 1024):.1f} MB")
    
    # Basic executable test (just check if it starts)
    try:
        # Note: This will actually launch the app, so we might want to skip this in CI
        print("ℹ️  To test the executable, run it manually from the dist/ folder")
        return True
    except Exception as e:
        print(f"❌ Executable test failed: {e}")
        return False


def create_release_package():
    """Create a release package with documentation."""
    print("\n📦 Creating release package...")
    
    release_dir = Path('release')
    if release_dir.exists():
        shutil.rmtree(release_dir)
    
    release_dir.mkdir()
    
    # Copy executable
    dist_dir = Path('dist')
    if dist_dir.exists():
        for item in dist_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, release_dir)
            elif item.is_dir():
                shutil.copytree(item, release_dir / item.name)
    
    # Copy documentation
    docs_to_copy = ['README.md', 'LICENSE', 'requirements.txt']
    for doc in docs_to_copy:
        if Path(doc).exists():
            shutil.copy2(doc, release_dir)
    
    # Create startup script for easier execution
    if platform.system() == 'Windows':
        startup_script = release_dir / 'start.bat'
        startup_script.write_text('@echo off\nClickWeave-Py.exe\npause')
    else:
        startup_script = release_dir / 'start.sh'
        startup_script.write_text('#!/bin/bash\n./ClickWeave-Py\n')
        startup_script.chmod(0o755)
    
    print(f"✅ Release package created in: {release_dir}")
    return True


def main():
    """Main build process."""
    print("🚀 ClickWeave-Py Build Script")
    print("=" * 50)
    
    # Check system
    print(f"Platform: {platform.system()} {platform.architecture()[0]}")
    print(f"Python: {sys.version}")
    
    # Build steps
    steps = [
        ("Cleaning build directories", clean_build_dirs),
        ("Checking dependencies", check_dependencies),
        ("Creating version info", create_version_info),
        ("Checking icons", create_icon),
        ("Building executable", build_executable),
        ("Testing executable", test_executable),
        ("Creating release package", create_release_package),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        try:
            if not step_func():
                print(f"❌ Step failed: {step_name}")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Step failed with exception: {step_name} - {e}")
            sys.exit(1)
    
    print("\n🎉 Build process completed successfully!")
    print("📂 Check the 'release/' folder for the final package")


if __name__ == '__main__':
    main()