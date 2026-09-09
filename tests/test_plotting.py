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


def test_matplotlib_hindi_and_english(tmp_path):
    fig_path = str(tmp_path / "plot.png").replace("\\", "/")
    code = f"""
    aayat matplotlib.pyplot ke_roop_mein plt

    plt.figure()
    plt.rekha([1, 2, 3], [4, 5, 6])
    plt.sheershak("Test Title")
    plt.x_namankit("X Axis")
    plt.y_namankit("Y Axis")
    plt.jaal(true)
    plt.chitra_bachao("{fig_path}")
    plt.band_karo()
    """
    run_code(code)
    assert os.path.exists(fig_path)


def test_seaborn_hindi():
    code = """
    aayat seaborn ke_roop_mein sns
    aayat matplotlib.pyplot ke_roop_mein plt

    maano data_x = [1, 2, 3, 4, 5]
    maano data_y = [5, 4, 3, 2, 1]

    maano ax = sns.rekha_chitra(x=data_x, y=data_y)
    plt.band_karo()
    """
    run_code(code)
