import os
import pytest
from lexer import tokenize
from ind_parser import parse
from interpreter import Interpreter


def run_code(code):
    interpreter = Interpreter()
    program = parse(tokenize(code))
    interpreter.run(program)
    return interpreter


def test_native_csv_helpers(tmp_path):
    csv_file = tmp_path / "people.csv"
    csv_path = str(csv_file).replace("\\", "/")

    code = f"""
    maano people = [
        {{"name": "Aarav", "age": 25}},
        {{"name": "Diya", "age": 30}}
    ]
    csv_likho("{csv_path}", people)

    maano loaded = csv_padho("{csv_path}")

    csv_jodo("{csv_path}", {{"name": "Kabir", "age": 22}})
    maano after_append = csv_padho("{csv_path}")
    """
    interp = run_code(code)
    loaded = interp.globals.get("loaded")
    assert len(loaded) == 2
    assert loaded[0]["name"] == "Aarav"

    after_append = interp.globals.get("after_append")
    assert len(after_append) == 3


def test_native_json_helpers(tmp_path):
    json_file = tmp_path / "config.json"
    json_path = str(json_file).replace("\\", "/")

    code = f"""
    maano config = {{"model": "random_forest", "n_estimators": 100, "enabled": true}}
    json_likho("{json_path}", config)

    maano read_config = json_padho("{json_path}")
    """
    interp = run_code(code)
    read_config = interp.globals.get("read_config")
    assert read_config["model"] == "random_forest"
    assert read_config["n_estimators"] == 100
    assert read_config["enabled"] is True
