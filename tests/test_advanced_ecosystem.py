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


def test_joblib_hindi_and_english(tmp_path):
    model_path = str(tmp_path / "model.joblib").replace("\\", "/")
    code = f"""
    aayat joblib

    maano payload = {{"weights": [1.0, 2.0, 3.0], "bias": 0.5}}
    joblib.bachao(payload, "{model_path}")

    maano loaded = joblib.bharit_karo("{model_path}")
    """
    interp = run_code(code)
    loaded = interp.globals.get("loaded")
    assert loaded["weights"] == [1.0, 2.0, 3.0]
    assert loaded["bias"] == 0.5


def test_sqlite3_integration(tmp_path):
    db_path = str(tmp_path / "test.db").replace("\\", "/")
    code = f"""
    aayat sqlite3

    maano conn = sqlite3.connect("{db_path}")
    maano cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    cur.execute("INSERT INTO users (name) VALUES ('Rohan')")
    conn.commit()

    cur.execute("SELECT name FROM users WHERE id = 1")
    maano row = cur.fetchone()
    conn.close()
    """
    interp = run_code(code)
    row = interp.globals.get("row")
    assert row[0] == "Rohan"


def test_torch_tensor_operations():
    try:
        import torch
    except ImportError:
        pytest.skip("PyTorch not installed")

    code = """
    aayat torch

    maano t = torch.tensor([1.0, 2.0, 3.0, 4.0])
    maano z = torch.zeros([2, 2])
    """
    interp = run_code(code)
    t = interp.globals.get("t")
    assert isinstance(t, torch.Tensor)
    assert t.shape == torch.Size([4])


def test_tensorflow_keras_components():
    try:
        import tensorflow as tf
        from tensorflow import keras
    except ImportError:
        pytest.skip("TensorFlow/Keras not installed")

    code = """
    aayat tensorflow ke_roop_mein tf
    se tensorflow aayat keras

    maano model = keras.Sequential()
    """
    interp = run_code(code)
    model = interp.globals.get("model")
    assert model is not None
