"""
© 2026 Darshil Vyas
All Rights Reserved.

This source code is part of a personal portfolio project.
It may not be copied, distributed, or used commercially
without explicit permission from the author.

For any queries regarding this project, feel free to contact me:
Email: darshilvyas7@gmail.com
LinkedIn: https://www.linkedin.com/in/darshil-vyas


"""


"""
Build script to convert pyside6.py to EXE with proper icon.
The EXE will auto-register for startup and create shortcuts on first run.
and also try to handle runtime errors while bundleing EXE...

"""

import os
import sys
import subprocess
from pathlib import Path

# Configuration 
APP_NAME = "PixelverseWallpaper"
SCRIPT_FILE = "pyside6.py"
ICON_FILE = "asset/logo.ico"
OUTPUT_DIR = "dist"
EXE_NAME = f"{APP_NAME}.exe"

def build_exe():
    # Build the EXE using PyInstaller
    print("Building EXE with PyInstaller...")
    
    # Get absolute paths
    icon_path = os.path.abspath(ICON_FILE)
    asset_path = os.path.abspath("asset")
    
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Single executable file EXE
        "--windowed",  # No console window
        f"--icon={icon_path}",  # Set icon with absolute path
        f"--name={APP_NAME}",  # Output name
        "--distpath", OUTPUT_DIR,  # Output directory
        "--specpath", "build",  # Spec directory
        "--workpath", "build/work",  # Work directory
        "--add-data", f"{asset_path}{os.pathsep}asset",  # Include asset folder with absolute path
        "--noupx",  # Disable UPX packing
        "-y",  # Automatically confirm building
        SCRIPT_FILE
    ]
    
    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
        # PyInstaller may fail on set_exe_build_timestamp with Python 3.14 but EXE is still created
        # It means Exe file is successfully creating but while timestamp phase it getting failed 
        if "set_exe_build_timestamp" in result.stderr and os.path.exists(get_exe_path()):
            print("[OK] EXE built successfully! (timestamp warning ignored)")
            return True
        elif result.returncode == 0 or os.path.exists(get_exe_path()):
            print("[OK] EXE built successfully..")
            return True
        else:
            print("[ERROR]Error building EXE: {0}".format(result.stderr[-500:] if len(result.stderr) > 500 else result.stderr))
            return False
    except Exception as e:
        print("[ERROR] Build exception: {0}".format(str(e)))
        return False

def get_exe_path():
    # Get the full path to the built EXE
    return os.path.join(OUTPUT_DIR, EXE_NAME)

def main():
    # Main build process...
    print("\n" + "="*50)
    print("Building {0}".format(APP_NAME))
    print("="*50 + "\n")
    
    # Build EXE
    if not build_exe():
        print("[ERROR]cBuild failed Exiting...")
        return False
    
    exe_path = get_exe_path()
    
    if not os.path.exists(exe_path):
        print("[ERROR] EXE not found at {0}".format(exe_path))
        return False
    
    print("\nEXE location: {0}\n".format(exe_path))
    
    print("\n" + "="*50)
    print("[OK] Build complete...")
    print("="*50)
    print("\nWhen users run the EXE File:")
    print("  --Auto-registers for Windows startup")
    print("  --Creates desktop shortcut(.lnk)")
    print("  --Shows app icon in taskbar")
    print("\nYou can now send {0} to others!".format(EXE_NAME))
    print("They just need to run it once everything auto-configures/\n")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
