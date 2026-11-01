from app import Figure


def test_broken_length():
    assert Figure("квадрат", 5).get_figure_length == 6


def test_after_broken():
    assert Figure("трикутник", 1).type == "трикутник"
