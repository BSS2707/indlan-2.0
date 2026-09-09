#!/usr/bin/env python3
"""
IndLan - A Hindi + English Programming Language for the Python Ecosystem.

Usage:
    indlan                             # launch IndLan IDE (or REPL)
    indlan ide                         # launch IndLan IDE
    indlan <file.ind>                  # run a file
    indlan run <file.ind>              # run a file
    indlan repl                        # start REPL
    indlan --version                   # print version
    indlan --help                      # print help
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer import tokenize, LexError
from ind_parser import parse, ParseError
from interpreter import Interpreter, IndLanRuntimeError
from py_bridge import IndLanImportError

__version__ = "2.1.1"


def print_banner():
    lines = [
        "Welcome to IndLan (v" + __version__ + ")",
        "Hindi + English Python Ecosystem Interface",
        "Made by Bhavya S Solanki",
    ]
    width = max(len(line) for line in lines) + 4
    top = "+" + "-" * (width - 2) + "+"
    print(top)
    for line in lines:
        padding = width - 2 - len(line)
        left = padding // 2
        right = padding - left
        print("|" + " " * left + line + " " * right + "|")
    print(top)


def run_source(source, interpreter):
    try:
        tokens = tokenize(source)
        program = parse(tokens)
        interpreter.run(program)
        return True
    except LexError as e:
        print(e, file=sys.stderr)
    except ParseError as e:
        print(e, file=sys.stderr)
    except IndLanImportError as e:
        print(e, file=sys.stderr)
    except IndLanRuntimeError as e:
        print(e, file=sys.stderr)
    except Exception as e:
        if getattr(interpreter, "debug", False):
            import traceback
            traceback.print_exc()
        else:
            print(f"[IndLan Runtime Error] {e}", file=sys.stderr)
    return False


def run_file(path, debug=False):
    if not os.path.exists(path):
        print(f"IndLan: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    interpreter = Interpreter(debug=debug)
    success = run_source(source, interpreter)
    if not success:
        sys.exit(1)


def run(source, debug=False, interpreter=None):
    """
    Run IndLan source code from Python.
    
    Args:
        source (str): IndLan source code to execute
        debug (bool): Enable debug mode with Python tracebacks
        interpreter (Interpreter): Optional existing interpreter instance
    
    Returns:
        bool: True if execution succeeded, False otherwise
    """
    if interpreter is None:
        interpreter = Interpreter(debug=debug)
    return run_source(source, interpreter)


def repl(debug=False):
    print_banner()
    print("IndLan REPL (type 'exit' to quit)")
    interpreter = Interpreter(debug=debug)
    while True:
        try:
            line = input("indlan> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line.strip() in ("exit", "quit"):
            break
        if not line.strip():
            continue
        run_source(line, interpreter)


def launch_ide():
    try:
        from indlan_ide import main as ide_main
        ide_main()
    except Exception as e:
        print(f"Failed to launch IndLan IDE: {e}", file=sys.stderr)
        repl()


def main():
    parser = argparse.ArgumentParser(
        prog="indlan",
        description="IndLan - Hindi + English Python Ecosystem Interface",
        add_help=False
    )
    parser.add_argument("command_or_file", nargs="?", default=None, help="File to run or command (ide, repl, run)")
    parser.add_argument("extra_file", nargs="?", default=None, help="File to run if command was 'run'")
    parser.add_argument("-v", "--version", action="store_true", help="Show IndLan version")
    parser.add_argument("-h", "--help", action="store_true", help="Show help message")
    parser.add_argument("--debug", action="store_true", help="Enable Python traceback on error")

    args = parser.parse_args()

    if args.version:
        print(f"IndLan version {__version__}")
        return

    if args.help:
        print_banner()
        print("""
Usage:
    indlan                             Launch IndLan Desktop IDE
    indlan ide                         Launch IndLan Desktop IDE
    indlan <file.ind>                  Execute an IndLan program file
    indlan run <file.ind>              Execute an IndLan program file
    indlan repl                        Start interactive REPL
    indlan --debug <file.ind>          Execute with detailed Python tracebacks
    indlan --version                   Show version
    indlan --help                      Show this help message

Examples:
    aayat pandas ke_roop_mein pd
    se sklearn.ensemble aayat RandomForestClassifier
    maano data = pd.csv_padho("students.csv")
    model.sikhao(X_train, y_train)
        """)
        return

    if args.command_or_file is None:
        launch_ide()
    elif args.command_or_file in ("ide", "gui"):
        launch_ide()
    elif args.command_or_file == "repl":
        repl(debug=args.debug)
    elif args.command_or_file == "run":
        if not args.extra_file:
            print("IndLan: missing file argument for 'run'", file=sys.stderr)
            sys.exit(1)
        run_file(args.extra_file, debug=args.debug)
    else:
        run_file(args.command_or_file, debug=args.debug)


if __name__ == "__main__":
    main()