import pytest
from lexer import tokenize
from ind_parser import parse
from interpreter import Interpreter, IndLanRuntimeError


def run_code_with_inputs(code, input_responses):
    responses = list(input_responses)
    prompts_received = []

    def mock_input(prompt=""):
        prompts_received.append(prompt)
        if not responses:
            raise EOFError("No more mock inputs available")
        return responses.pop(0)

    interp = Interpreter(input_func=mock_input)
    program = parse(tokenize(code))
    interp.run(program)
    return interp, prompts_received


def test_aalao_and_input():
    code = """
    maano a = aalao("Enter name: ")
    maano b = input("Enter city: ")
    maano c = aalao()
    """
    interp, prompts = run_code_with_inputs(code, ["Bhavya", "Mumbai", "Test"])
    assert interp.globals.get("a") == "Bhavya"
    assert interp.globals.get("b") == "Mumbai"
    assert interp.globals.get("c") == "Test"
    assert prompts == ["Enter name: ", "Enter city: ", ""]


def test_number_dalao_and_input_int():
    code = """
    maano age = number_dalao("Umar: ")
    maano count = input_int("Count: ")
    maano negative = number_dalao("Neg: ")
    """
    interp, prompts = run_code_with_inputs(code, ["25", " 100 ", "-42"])
    assert interp.globals.get("age") == 25
    assert isinstance(interp.globals.get("age"), int)
    assert interp.globals.get("count") == 100
    assert interp.globals.get("negative") == -42


def test_number_dalao_invalid():
    code = """
    maano x = number_dalao("Enter num: ")
    """
    with pytest.raises(IndLanRuntimeError, match="Invalid integer input"):
        run_code_with_inputs(code, ["abc"])

    with pytest.raises(IndLanRuntimeError, match="Invalid integer input"):
        run_code_with_inputs(code, ["12.34"])


def test_decimal_dalao_and_input_float():
    code = """
    maano height = decimal_dalao("Height: ")
    maano pi_val = input_float("Pi: ")
    maano int_as_float = decimal_dalao()
    """
    interp, prompts = run_code_with_inputs(code, ["5.9", " 3.14159 ", "10"])
    assert interp.globals.get("height") == 5.9
    assert isinstance(interp.globals.get("height"), float)
    assert interp.globals.get("pi_val") == 3.14159
    assert interp.globals.get("int_as_float") == 10.0
    assert isinstance(interp.globals.get("int_as_float"), float)


def test_decimal_dalao_invalid():
    code = """
    maano x = decimal_dalao("Enter float: ")
    """
    with pytest.raises(IndLanRuntimeError, match="Invalid float input"):
        run_code_with_inputs(code, ["xyz"])


def test_haan_na_and_input_bool():
    code = """
    maano t1 = haan_na("Continue? ")
    maano t2 = input_bool("Is ok? ")
    maano t3 = haan_na("Sahi? ")
    maano t4 = haan_na("Haan? ")
    maano t5 = haan_na("Yes? ")
    maano t6 = haan_na("1? ")

    maano f1 = haan_na("Stop? ")
    maano f2 = input_bool("Not ok? ")
    maano f3 = haan_na("Galat? ")
    maano f4 = haan_na("Na? ")
    maano f5 = haan_na("No? ")
    maano f6 = haan_na("0? ")
    """
    inputs = [
        "true", "True", "sahi", "haan", "YES", "1",
        "false", "False", "galat", "na", "NO", "0"
    ]
    interp, _ = run_code_with_inputs(code, inputs)
    for var in ["t1", "t2", "t3", "t4", "t5", "t6"]:
        assert interp.globals.get(var) is True
    for var in ["f1", "f2", "f3", "f4", "f5", "f6"]:
        assert interp.globals.get(var) is False


def test_haan_na_invalid():
    code = """
    maano x = haan_na("Continue? ")
    """
    with pytest.raises(IndLanRuntimeError, match="Invalid boolean input"):
        run_code_with_inputs(code, ["maybe"])

    with pytest.raises(IndLanRuntimeError, match="Invalid boolean input"):
        run_code_with_inputs(code, ["invalid_val"])


def test_user_request_full_example():
    code = """
    maano naam = aalao("Apna naam: ")
    maano umar = number_dalao("Umar: ")
    maano height = decimal_dalao("Height: ")
    maano pass = haan_na("Continue? (true/false): ")
    """
    interp, prompts = run_code_with_inputs(code, ["Aarav", "21", "5.11", "true"])
    assert interp.globals.get("naam") == "Aarav"
    assert interp.globals.get("umar") == 21
    assert interp.globals.get("height") == 5.11
    assert interp.globals.get("pass") is True
    assert prompts == [
        "Apna naam: ",
        "Umar: ",
        "Height: ",
        "Continue? (true/false): "
    ]
