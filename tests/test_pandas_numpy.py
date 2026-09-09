import os
import pytest
import pandas as pd
import numpy as np
from lexer import tokenize
from ind_parser import parse
from interpreter import Interpreter


def run_code(code):
    interpreter = Interpreter()
    program = parse(tokenize(code))
    interpreter.run(program)
    return interpreter


def test_numpy_hindi_and_english():
    code = """
    aayat numpy ke_roop_mein np

    maano arr = np.sarni([10, 20, 30, 40])
    maano m = np.madhya(arr)
    maano total = np.yog(arr)
    maano zeroes = np.shunya(5)
    maano reshaped = np.aakar_badlo(arr, [2, 2])
    """
    interp = run_code(code)
    arr = interp.globals.get("arr")
    assert isinstance(arr, np.ndarray)
    assert interp.globals.get("m") == 25.0
    assert interp.globals.get("total") == 100
    assert len(interp.globals.get("zeroes")) == 5
    assert interp.globals.get("reshaped").shape == (2, 2)


def test_pandas_hindi_and_english(tmp_path):
    csv_file = tmp_path / "students.csv"
    csv_file.write_text("name,marks\nAmit,85\nPriya,92\nRahul,78\n", encoding="utf-8")
    csv_path_str = str(csv_file).replace("\\", "/")

    code = f"""
    aayat pandas ke_roop_mein pd

    maano data = pd.csv_padho("{csv_path_str}")
    maano head_rows = data.shuru_ke(2)
    maano rows_shape = data.shape
    maano desc = data.vivaran()
    """
    interp = run_code(code)
    data = interp.globals.get("data")
    assert isinstance(data, pd.DataFrame)
    assert len(data) == 3
    assert len(interp.globals.get("head_rows")) == 2
    assert interp.globals.get("rows_shape") == (3, 2)
