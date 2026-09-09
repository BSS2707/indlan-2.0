import os
import pytest
import matplotlib
matplotlib.use("Agg")
from lexer import tokenize
from ind_parser import parse
from interpreter import Interpreter


def run_code(code):
    interpreter = Interpreter()
    program = parse(tokenize(code))
    interpreter.run(program)
    return interpreter


def test_section_35_hindi_example(tmp_path):
    csv_file = tmp_path / "students.csv"
    csv_file.write_text("feature1,feature2,target\n1,2,0\n2,3,0\n3,4,0\n4,5,0\n5,6,1\n6,7,1\n7,8,1\n8,9,1\n", encoding="utf-8")
    csv_path = str(csv_file).replace("\\", "/")

    code = f"""
    aayat pandas ke_roop_mein pd
    aayat numpy ke_roop_mein np
    aayat matplotlib.pyplot ke_roop_mein plt

    se sklearn.model_selection aayat train_test_split
    se sklearn.ensemble aayat RandomForestClassifier

    maano raw_data = pd.csv_padho("{csv_path}")

    maano X_data = np.sarni([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9]])
    maano y_data = np.sarni([0, 0, 0, 0, 1, 1, 1, 1])

    maano X_train, X_test, y_train, y_test = train_test_split(
        X_data,
        y_data,
        test_size=0.25,
        random_state=42
    )

    maano model = RandomForestClassifier(random_state=42)

    model.sikhao(X_train, y_train)

    maano prediction = model.bhavishyavani(X_test)

    plt.figure()
    plt.rekha(prediction)
    plt.sheershak("Prediction")
    plt.jaal(true)
    plt.band_karo()
    """
    interp = run_code(code)
    pred = interp.globals.get("prediction")
    assert len(pred) == 2


def test_section_35_english_example(tmp_path):
    csv_file = tmp_path / "students.csv"
    csv_file.write_text("feature1,feature2,target\n1,2,0\n2,3,0\n3,4,0\n4,5,0\n5,6,1\n6,7,1\n7,8,1\n8,9,1\n", encoding="utf-8")
    csv_path = str(csv_file).replace("\\", "/")

    code = f"""
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier

    data = pd.read_csv("{csv_path}")

    X_data = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9]])
    y_data = np.array([0, 0, 0, 0, 1, 1, 1, 1])

    X_train, X_test, y_train, y_test = train_test_split(
        X_data,
        y_data,
        test_size=0.25,
        random_state=42
    )

    model = RandomForestClassifier(random_state=42)

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    plt.figure()
    plt.plot(prediction)
    plt.title("Prediction")
    plt.grid(true)
    plt.close()
    """
    interp = run_code(code)
    pred = interp.globals.get("prediction")
    assert len(pred) == 2
