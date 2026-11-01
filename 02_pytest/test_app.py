import pytest

from app import Figure

FIGURE_IDS = {"квадрат": "square", "прямокутник": "rectangle", "трикутник": "triangle"}


@pytest.fixture
def square():
    return Figure("квадрат", 5)


@pytest.fixture
def length():
    return 10


@pytest.fixture
def square_10(length):
    return Figure("квадрат", length)


@pytest.mark.unit
def test_triangle_type():
    assert Figure("трикутник", 4).type == "трикутник"


@pytest.mark.parametrize("figure_type", Figure.FIGURES, ids=lambda value: FIGURE_IDS[value])
def test_allowed_figure(figure_type):
    assert Figure(figure_type, 1).type == figure_type


@pytest.mark.parametrize("length", [1, 5, 10])
@pytest.mark.parametrize("figure_type", Figure.FIGURES, ids=lambda value: FIGURE_IDS[value])
def test_allowed_figure_length(figure_type, length):
    assert Figure(figure_type, length).get_figure_length == length


@pytest.mark.unit
def test_square_length(square):
    assert square.get_figure_length == 5


def test_square_10_properties(square_10):
    assert square_10.type == "квадрат"
    assert square_10.get_figure_length == 10


def test_length_fixture_dependency(length, square_10):
    assert square_10.get_figure_length == length


def test_invalid_figure():
    with pytest.raises(AssertionError):
        Figure("коло", 1)


def test_invalid_length():
    with pytest.raises(AssertionError):
        Figure("квадрат", 0)


@pytest.mark.parametrize(
    "figure_type",
    ["коло", "ромб", "", "КВАДРАТ"],
    ids=["circle", "rhombus", "empty", "upper_case"],
)
def test_invalid_figure_type(figure_type):
    with pytest.raises(AssertionError, match="Невідомий тип фігури"):
        Figure(figure_type, 1)


@pytest.mark.parametrize("length", [0, -1, -100])
def test_invalid_length_value(length):
    with pytest.raises(AssertionError, match="Довжина має бути більшою за 0"):
        Figure("квадрат", length)


def test_allowed_figures_count(allowed_figures):
    assert len(allowed_figures) == 3


def test_allowed_figures_content(allowed_figures):
    assert "квадрат" in allowed_figures
