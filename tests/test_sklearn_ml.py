import pytest
from lexer import tokenize
from ind_parser import parse
from interpreter import Interpreter


def run_code(code):
    interpreter = Interpreter()
    program = parse(tokenize(code))
    interpreter.run(program)
    return interpreter


def test_sklearn_workflow_hindi():
    code = """
    aayat numpy ke_roop_mein np
    se sklearn.ensemble aayat RandomForestClassifier
    se sklearn.model_selection aayat train_test_split
    se sklearn.metrics aayat satikta_ank

    maano X = np.sarni([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9]])
    maano y = np.sarni([0, 0, 0, 0, 1, 1, 1, 1])

    maano X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    maano model = RandomForestClassifier(random_state=42)
    model.sikhao(X_train, y_train)

    maano preds = model.bhavishyavani(X_test)
    maano acc = satikta_ank(y_test, preds)
    """
    interp = run_code(code)
    preds = interp.globals.get("preds")
    acc = interp.globals.get("acc")
    assert len(preds) == 2
    assert acc >= 0.0


def test_sklearn_workflow_english():
    code = """
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    X = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9]])
    y = np.array([0, 0, 0, 0, 1, 1, 1, 1])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    """
    interp = run_code(code)
    preds = interp.globals.get("preds")
    acc = interp.globals.get("acc")
    assert len(preds) == 2
    assert acc >= 0.0
