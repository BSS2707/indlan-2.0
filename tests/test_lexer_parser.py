import pytest
from lexer import tokenize
from ind_parser import parse
from ast_nodes import ImportStmt, FromImportStmt, LetStmt, KeywordArg, Call, Assign


def test_import_english():
    code = "import pandas as pd"
    tokens = tokenize(code)
    program = parse(tokens)
    assert len(program.statements) == 1
    stmt = program.statements[0]
    assert isinstance(stmt, ImportStmt)
    assert stmt.module_path == "pandas"
    assert stmt.alias == "pd"


def test_import_hindi():
    code = "aayat pandas ke_roop_mein pd"
    tokens = tokenize(code)
    program = parse(tokens)
    assert len(program.statements) == 1
    stmt = program.statements[0]
    assert isinstance(stmt, ImportStmt)
    assert stmt.module_path == "pandas"
    assert stmt.alias == "pd"


def test_dot_import_hindi():
    code = "aayat matplotlib.pyplot ke_roop_mein plt"
    tokens = tokenize(code)
    program = parse(tokens)
    stmt = program.statements[0]
    assert isinstance(stmt, ImportStmt)
    assert stmt.module_path == "matplotlib.pyplot"
    assert stmt.alias == "plt"


def test_from_import_english():
    code = "from sklearn.ensemble import RandomForestClassifier"
    tokens = tokenize(code)
    program = parse(tokens)
    stmt = program.statements[0]
    assert isinstance(stmt, FromImportStmt)
    assert stmt.module_path == "sklearn.ensemble"
    assert stmt.items == [("RandomForestClassifier", None)]


def test_from_import_hindi():
    code = "se sklearn.ensemble aayat RandomForestClassifier"
    tokens = tokenize(code)
    program = parse(tokens)
    stmt = program.statements[0]
    assert isinstance(stmt, FromImportStmt)
    assert stmt.module_path == "sklearn.ensemble"
    assert stmt.items == [("RandomForestClassifier", None)]


def test_multi_variable_let():
    code = "maano X_train, X_test, y_train, y_test = split_data()"
    tokens = tokenize(code)
    program = parse(tokens)
    stmt = program.statements[0]
    assert isinstance(stmt, LetStmt)
    assert stmt.names == ["X_train", "X_test", "y_train", "y_test"]


def test_keyword_arguments():
    code = "model.sikhao(X_train, y_train, epochs=10, batch_size=32)"
    tokens = tokenize(code)
    program = parse(tokens)
    call_node = program.statements[0].expr
    assert isinstance(call_node, Call)
    assert len(call_node.args) == 4
    assert isinstance(call_node.args[2], KeywordArg)
    assert call_node.args[2].name == "epochs"
    assert call_node.args[2].value.value == 10
    assert isinstance(call_node.args[3], KeywordArg)
    assert call_node.args[3].name == "batch_size"
    assert call_node.args[3].value.value == 32
