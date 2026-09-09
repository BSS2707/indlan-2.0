#!/usr/bin/env python3
"""
Build script to compile IndLan 2.1 executables using PyInstaller:
- dist/IndLan_IDE.exe (GUI IDE standalone executable - VSCode Edition)
- dist/IndLan.exe (CLI interpreter executable)
"""

import sys
import os
import subprocess
import shutil


def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)
    print("Build directories cleaned.")


def build():
    root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root)

    print("=== Building IndLan 2.1 VSCode Edition Executables ===")
    
    # Clean previous builds
    clean_build_dirs()

    excludes = [
        "pandas", "numpy", "matplotlib", "seaborn", "scipy", "sklearn", "scikit-learn",
        "tensorflow", "keras", "torch", "torchvision", "transformers", "spacy", "nltk",
        "plotly", "openpyxl", "xlsxwriter", "joblib", "PIL", "pillow", "cv2",
        "cryptography", "charset_normalizer", "urllib3", "requests", "certifi",
        "IPython", "pytest", "setuptools", "wheel", "pip", "pycparser", "cffi", "pydantic",
        "pydantic_core", "rich", "typer", "click"
    ]
    exclude_args = []
    for ex in excludes:
        exclude_args.extend(["--exclude-module", ex])

    # 1. Build IndLan CLI executable (dist/IndLan.exe)
    print("\n[1/2] Building IndLan CLI Executable (IndLan.exe)...")
    cli_cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--icon",
        "indlan_icon.ico" if os.path.exists("indlan_icon.ico") else None,
        "--name",
        "IndLan",
        "--add-data",
        "README.md:.",
        *exclude_args,
        "indlan.py",
    ]
    # Remove None values
    cli_cmd = [arg for arg in cli_cmd if arg is not None]
    
    res1 = subprocess.run(cli_cmd)
    if res1.returncode != 0:
        print("Failed to build IndLan.exe", file=sys.stderr)
        sys.exit(res1.returncode)

    # 2. Build IndLan IDE executable (dist/IndLan_IDE.exe)
    print("\n[2/2] Building IndLan 2.1 VSCode Edition Desktop GUI IDE Executable (IndLan_IDE.exe)...")
    ide_cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        "--icon",
        "indlan_icon.ico" if os.path.exists("indlan_icon.ico") else None,
        "--name",
        "IndLan_IDE",
        "--add-data",
        "README.md:.",
        *exclude_args,
        "indlan_ide.py",
    ]
    # Remove None values
    ide_cmd = [arg for arg in ide_cmd if arg is not None]
    
    res2 = subprocess.run(ide_cmd)
    if res2.returncode != 0:
        print("Failed to build IndLan_IDE.exe", file=sys.stderr)
        sys.exit(res2.returncode)

    print("\n=======================================================")
    print("[+] Build Complete! Executables created in 'dist/':")
    print(f"  * {os.path.join(root, 'dist', 'IndLan.exe')}")
    print(f"  * {os.path.join(root, 'dist', 'IndLan_IDE.exe')}")
    print("\n[+] IndLan 2.1 VSCode Edition ready for distribution!")
    print("=======================================================")


if __name__ == "__main__":
    build()
