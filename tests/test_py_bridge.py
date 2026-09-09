import pytest
from lexer import tokenize
from ind_parser import parse
from interpreter import Interpreter
from py_bridge import IndLanImportError, format_missing_package_error


def run_code(code):
    interpreter = Interpreter()
    program = parse(tokenize(code))
    interpreter.run(program)
    return interpreter


def test_missing_package_error_format():
    err_msg = format_missing_package_error("nonexistent_pkg_xyz")
    assert "[IndLan Import Error]" in err_msg
    assert "Package 'nonexistent_pkg_xyz' is not installed." in err_msg
    assert "pip install nonexistent_pkg_xyz" in err_msg
    assert 'pip install "indlan[full]"' in err_msg

    pandas_err = format_missing_package_error("pandas")
    assert 'pip install "indlan[data]"' in pandas_err

    sklearn_err = format_missing_package_error("sklearn")
    assert 'pip install "indlan[ml]"' in sklearn_err

    torch_err = format_missing_package_error("torch")
    assert 'pip install "indlan[ai]"' in torch_err


def test_missing_package_execution():
    code = "aayat non_existent_library_12345 ke_roop_mein nel"
    with pytest.raises(IndLanImportError) as exc_info:
        run_code(code)
    assert "[IndLan Import Error]" in str(exc_info.value)
    assert "non_existent_library_12345" in str(exc_info.value)


def test_math_ganit_aliases():
    code = """
    aayat math ke_roop_mein ganit
    maano root = ganit.vargmool(16)
    maano power = ganit.ghat(2, 3)
    maano flr = ganit.neeche_purnank(3.7)
    maano cl = ganit.upar_purnank(3.2)
    maano pi_val = ganit.pai
    """
    interp = run_code(code)
    assert interp.globals.get("root") == 4.0
    assert interp.globals.get("power") == 8.0
    assert interp.globals.get("flr") == 3
    assert interp.globals.get("cl") == 4
    import math
    assert interp.globals.get("pi_val") == math.pi
