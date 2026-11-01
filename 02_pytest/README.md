# Звіт до роботи

**Тема:** Тестування з використанням бібліотеки pytest

**Мета роботи:** навчитись писати тести у вигляді звичайних функцій за допомогою pytest, використовувати `pytest.raises`, параметризацію, fixtures, маркери та корисні параметри запуску.

**Виконав:** Бейгул Володимир, група КН-42

## Виконання роботи

### Встановлення pytest

```bash
pip install pytest
```

У моєму середовищі команди запускались через `py -m pytest`, це те саме, що `pytest`. Версія:

```text
pytest 9.2.0
```

### Структура проєкту

```text
02_pytest/
├── app.py                 клас Figure
├── conftest.py            спільна fixture allowed_figures (scope="module")
├── test_app.py            тести
├── broken_examples/
│   └── test_broken.py     навмисно зламаний тест
├── build_report.py        генерує цей звіт зі справжніх запусків
├── pyproject.toml         налаштування pytest, маркер unit
└── Makefile
```

### Основи: assert та pytest.raises

Клас `Figure` з прикладу:

```python
class Figure:
    FIGURES = ["квадрат", "прямокутник", "трикутник"]

    def __init__(self, figure_type: str, length: int) -> None:
        assert length > 0, "Довжина має бути більшою за 0!"
        assert figure_type in self.FIGURES, "Невідомий тип фігури"
        self.type = figure_type
        self.length = length

    @property
    def get_figure_length(self) -> int:
        return self.length
```

Тести у `test_app.py`:

```python
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
```

Запуск усіх тестів `pytest -v`:

```text
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\rrete\AppData\Local\Python\pythoncore-3.15-64\python.exe
cachedir: .pytest_cache
rootdir: D:\Microsoft VS Code\02_pytest
configfile: pyproject.toml
testpaths: .
collecting ... collected 27 items

test_app.py::test_triangle_type PASSED                                   [  3%]
test_app.py::test_allowed_figure[square] PASSED                          [  7%]
test_app.py::test_allowed_figure[rectangle] PASSED                       [ 11%]
test_app.py::test_allowed_figure[triangle] PASSED                        [ 14%]
test_app.py::test_allowed_figure_length[square-1] PASSED                 [ 18%]
test_app.py::test_allowed_figure_length[square-5] PASSED                 [ 22%]
test_app.py::test_allowed_figure_length[square-10] PASSED                [ 25%]
test_app.py::test_allowed_figure_length[rectangle-1] PASSED              [ 29%]
test_app.py::test_allowed_figure_length[rectangle-5] PASSED              [ 33%]
test_app.py::test_allowed_figure_length[rectangle-10] PASSED             [ 37%]
test_app.py::test_allowed_figure_length[triangle-1] PASSED               [ 40%]
test_app.py::test_allowed_figure_length[triangle-5] PASSED               [ 44%]
test_app.py::test_allowed_figure_length[triangle-10] PASSED              [ 48%]
test_app.py::test_square_length PASSED                                   [ 51%]
test_app.py::test_square_10_properties PASSED                            [ 55%]
test_app.py::test_length_fixture_dependency PASSED                       [ 59%]
test_app.py::test_invalid_figure PASSED                                  [ 62%]
test_app.py::test_invalid_length PASSED                                  [ 66%]
test_app.py::test_invalid_figure_type[circle] PASSED                     [ 70%]
test_app.py::test_invalid_figure_type[rhombus] PASSED                    [ 74%]
test_app.py::test_invalid_figure_type[empty] PASSED                      [ 77%]
test_app.py::test_invalid_figure_type[upper_case] PASSED                 [ 81%]
test_app.py::test_invalid_length_value[0] PASSED                         [ 85%]
test_app.py::test_invalid_length_value[-1] PASSED                        [ 88%]
test_app.py::test_invalid_length_value[-100] PASSED                      [ 92%]
test_app.py::test_allowed_figures_count PASSED                           [ 96%]
test_app.py::test_allowed_figures_content PASSED                         [100%]

============================= 27 passed in 0.06s ==============================
```

Запуск одного тесту `pytest test_app.py::test_triangle_type -v`:

```text
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\rrete\AppData\Local\Python\pythoncore-3.15-64\python.exe
cachedir: .pytest_cache
rootdir: D:\Microsoft VS Code\02_pytest
configfile: pyproject.toml
collecting ... collected 1 item

test_app.py::test_triangle_type PASSED                                   [100%]

============================== 1 passed in 0.04s ==============================
```

### Параметризація та fixtures

⭐ **Параметризований тест для всіх дозволених фігур.** `test_allowed_figure` виконується окремо для кожного типу з `Figure.FIGURES`. Тест `test_allowed_figure_length` поєднує два `parametrize`, тож перевіряється кожна комбінація типу й довжини (3 × 3 = 9 запусків). Для зрозумілих назв у виводі задано `ids` (square, rectangle, triangle).

⭐ **Fixture з довжиною 10.** Fixture `length` повертає 10, а `square_10` залежить від неї й створює квадрат. Тест `test_square_10_properties` перевіряє тип і довжину, а `test_length_fixture_dependency` показує, що залежна fixture отримує те саме значення.

🔥 **Тести для неправильних даних.** `test_invalid_figure_type` перевіряє кожен неправильний тип (`коло`, `ромб`, порожній рядок, `КВАДРАТ`), а `test_invalid_length_value` кожне неправильне значення довжини (0, -1, -100). У `pytest.raises` використано `match`, тому перевіряється й текст повідомлення, а не лише тип винятку.

### Розширені можливості

⭐ **Маркер `unit`.** Маркер додано до двох тестів (`test_triangle_type`, `test_square_length`) і зареєстровано в `pyproject.toml`. Запуск лише їх, `pytest -m unit -v`:

```text
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\rrete\AppData\Local\Python\pythoncore-3.15-64\python.exe
cachedir: .pytest_cache
rootdir: D:\Microsoft VS Code\02_pytest
configfile: pyproject.toml
testpaths: .
collecting ... collected 27 items / 25 deselected / 2 selected

test_app.py::test_triangle_type PASSED                                   [ 50%]
test_app.py::test_square_length PASSED                                   [100%]

====================== 2 passed, 25 deselected in 0.04s =======================
```

⭐ **Fixture зі `scope="module"`.** У `conftest.py` fixture `allowed_figures` має область дії `module`, тобто pytest створює її один раз для модуля. Її використовують два тести: `test_allowed_figures_count` і `test_allowed_figures_content`. Оскільки fixture лежить у `conftest.py`, імпортувати її в тести не потрібно.

Команда `pytest --collect-only` показує всі знайдені тести без їх виконання:

```text
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0
rootdir: D:\Microsoft VS Code\02_pytest
configfile: pyproject.toml
testpaths: .
collected 27 items

<Dir 02_pytest>
  <Module test_app.py>
    <Function test_triangle_type>
    <Function test_allowed_figure[square]>
    <Function test_allowed_figure[rectangle]>
    <Function test_allowed_figure[triangle]>
    <Function test_allowed_figure_length[square-1]>
    <Function test_allowed_figure_length[square-5]>
    <Function test_allowed_figure_length[square-10]>
    <Function test_allowed_figure_length[rectangle-1]>
    <Function test_allowed_figure_length[rectangle-5]>
    <Function test_allowed_figure_length[rectangle-10]>
    <Function test_allowed_figure_length[triangle-1]>
    <Function test_allowed_figure_length[triangle-5]>
    <Function test_allowed_figure_length[triangle-10]>
    <Function test_square_length>
    <Function test_square_10_properties>
    <Function test_length_fixture_dependency>
    <Function test_invalid_figure>
    <Function test_invalid_length>
    <Function test_invalid_figure_type[circle]>
    <Function test_invalid_figure_type[rhombus]>
    <Function test_invalid_figure_type[empty]>
    <Function test_invalid_figure_type[upper_case]>
    <Function test_invalid_length_value[0]>
    <Function test_invalid_length_value[-1]>
    <Function test_invalid_length_value[-100]>
    <Function test_allowed_figures_count>
    <Function test_allowed_figures_content>

========================= 27 tests collected in 0.04s =========================
```

🔥 **Навмисно зламаний тест.** У `broken_examples/test_broken.py` тест `test_broken_length` очікує довжину 6 замість 5. Запуск `pytest broken_examples/test_broken.py -x --tb=short`:

```text
============================= test session starts =============================
platform win32 -- Python 3.15.2, pytest-9.2.0, pluggy-1.7.0
rootdir: D:\Microsoft VS Code\02_pytest
configfile: pyproject.toml
collected 2 items

broken_examples\test_broken.py F

================================== FAILURES ===================================
_____________________________ test_broken_length ______________________________
broken_examples\test_broken.py:5: in test_broken_length
    assert Figure("квадрат", 5).get_figure_length == 6
E   AssertionError: assert 5 == 6
E    +  where 5 = <app.Figure object at 0x0000015C8822FCB0>.get_figure_length
E    +    where <app.Figure object at 0x0000015C8822FCB0> = Figure('квадрат', 5)
=========================== short test summary info ===========================
FAILED broken_examples/test_broken.py::test_broken_length - AssertionError: a...
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!
============================== 1 failed in 0.11s ==============================
```

Пояснення: тест не проходить, бо порівняння `get_figure_length == 6` хибне, а реальне значення 5. Параметр `-x` зупиняє запуск після першої помилки, тому другий тест `test_after_broken` не виконується. Параметр `--tb=short` скорочує traceback до рядка з кодом і причини помилки. Папку `broken_examples` виключено з автоматичного пошуку тестів (`norecursedirs`), тому звичайний `pytest -v` її не запускає.

### Різниця між `unittest.TestCase` і pytest

| | `unittest.TestCase` | pytest |
|---|---|---|
| Форма тесту | метод у класі, що наслідує `TestCase` | звичайна функція `test_...` |
| Перевірки | методи `assertEqual`, `assertTrue` та інші | звичайний `assert` |
| Винятки | `self.assertRaises` | `pytest.raises` |
| Підготовка даних | `setUp`, `tearDown` | fixtures, які тест підключає через аргумент |
| Кілька наборів даних | `subTest` у циклі | `@pytest.mark.parametrize` |
| Запуск | `python -m unittest` | `pytest`, із фільтрами за маркером і назвою |

Тест у pytest коротший, бо не потрібен клас і спеціальні методи порівняння, а при помилці pytest сам показує значення з обох боків `assert`.

## Висновок

Виконав усі завдання роботи, включно з ⭐ та 🔥: параметризовані тести для всіх фігур, fixtures (зокрема залежну та зі `scope="module"`), маркер `unit`, тести для кожного неправильного типу й значення довжини, навмисно зламаний тест із `-x --tb=short`. Усі 27 тестів проходять.

Мети роботи досягнуто: навчився писати тести в pytest, використовувати `pytest.raises`, `parametrize`, fixtures, маркери та `conftest.py`.

Складності: pytest показує закодовані `\uXXXX` замість кирилиці в назвах параметризованих тестів, тому задав `ids` латиницею.

Feedback: формат здачі через посилання на репозиторій зручний, бо код, тести та звіт лежать разом.

Suggestions: додати в завдання приклад із `monkeypatch` або `capsys`, про які йдеться в описі.
