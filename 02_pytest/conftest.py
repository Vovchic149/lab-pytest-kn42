import pytest

from app import Figure


@pytest.fixture(scope="module")
def allowed_figures():
    return Figure.FIGURES
