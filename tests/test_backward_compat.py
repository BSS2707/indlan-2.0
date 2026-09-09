import os
import pytest
from lexer import tokenize
from ind_parser import parse
from interpreter import Interpreter


def test_examples_hindi():
    path = os.path.join(os.path.dirname(__file__), "..", "examples_hindi.ind")
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    interpreter = Interpreter()
    program = parse(tokenize(source))
    interpreter.run(program)
    assert interpreter.globals.get("umar") == 20
    assert interpreter.globals.get("din") == 3


def test_examples_ifelse():
    path = os.path.join(os.path.dirname(__file__), "..", "examples_ifelse.ind")
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    interpreter = Interpreter()
    program = parse(tokenize(source))
    interpreter.run(program)
