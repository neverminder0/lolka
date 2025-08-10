# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.absolute()

# Analysis block for the main script
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # Include data directories
        ('app/data', 'app/data'),
        # Include any assets (if they exist)
        ('app/assets', 'app/assets') if os.path.exists('app/assets') else None,
    ],
    hiddenimports=[
        # Core modules that PyInstaller might miss
        'customtkinter',
        'pynput',
        'pyautogui',
        'keyboard',
        'PIL',
        'PIL.Image',
        'PIL.ImageGrab',
        'mss',
        'apscheduler',
        'apscheduler.schedulers.background',
        'apscheduler.triggers.date',
        'apscheduler.triggers.interval', 
        'apscheduler.triggers.cron',
        'apscheduler.jobstores.memory',
        'apscheduler.executors.pool',
        'pydantic',
        'psutil',
        'threading',
        'queue',
        'uuid',
        'json',
        'csv',
        'datetime',
        'time',
        'logging',
        'pathlib',
        
        # Platform-specific modules
        'pynput._util.win32' if sys.platform == 'win32' else None,
        'pynput._util.darwin' if sys.platform == 'darwin' else None,
        'pynput._util.xorg' if sys.platform.startswith('linux') else None,
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'jupyter',
        'IPython',
        'pytest',
        'sphinx',
        'setuptools',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Filter out None values from datas
a.datas = [item for item in a.datas if item is not None]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Executable configuration
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ClickWeave-Py',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Use UPX compression to reduce size
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Windows specific options
    icon='app/assets/icon.ico' if os.path.exists('app/assets/icon.ico') else None,
    version_file='version_info.txt' if os.path.exists('version_info.txt') else None,
    # macOS specific options
    bundle_identifier='com.clickweave.autoclicker' if sys.platform == 'darwin' else None,
)

# macOS App Bundle (optional)
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='ClickWeave-Py.app',
        icon='app/assets/icon.icns' if os.path.exists('app/assets/icon.icns') else None,
        bundle_identifier='com.clickweave.autoclicker',
        info_plist={
            'CFBundleName': 'ClickWeave-Py',
            'CFBundleDisplayName': 'ClickWeave-Py Auto-clicker',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'NSHighResolutionCapable': True,
            'LSApplicationCategoryType': 'public.app-category.productivity',
            'NSHumanReadableCopyright': 'Copyright © 2024 ClickWeave-Py',
            'NSAppleEventsUsageDescription': 'This app needs to control other applications for automation.',
            'NSAppleScriptEnabled': True,
        }
    )