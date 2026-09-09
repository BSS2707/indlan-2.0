import sys
import subprocess
import pytest


def test_cli_version():
    result = subprocess.run([sys.executable, "indlan.py", "--version"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "IndLan version 2.0.0" in result.stdout


def test_cli_help():
    result = subprocess.run([sys.executable, "indlan.py", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "IndLan" in result.stdout
    assert "Usage:" in result.stdout


def test_cli_run_file(tmp_path):
    ind_file = tmp_path / "hello.ind"
    ind_file.write_text('chhap("Namaste IndLan!")\n', encoding="utf-8")
    result = subprocess.run([sys.executable, "indlan.py", str(ind_file)], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Namaste IndLan!" in result.stdout


def test_cli_run_command_subcommand(tmp_path):
    ind_file = tmp_path / "calc.ind"
    ind_file.write_text('maano x = 10 + 20\nchhap("Result:", x)\n', encoding="utf-8")
    result = subprocess.run([sys.executable, "indlan.py", "run", str(ind_file)], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Result: 30" in result.stdout
