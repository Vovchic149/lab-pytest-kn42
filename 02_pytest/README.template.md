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
{{CMD:VERSION}}
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
{{FILE:app.py}}
```

Тести у `test_app.py`:

```python
{{FILE:test_app.py}}
```

Запуск усіх тестів `pytest -v`:

```text
{{CMD:VERBOSE}}
```

{{IMG:pictures/01_pytest_v.png|Результат pytest -v}}

Запуск одного тесту `pytest test_app.py::test_triangle_type -v`:

```text
{{CMD:ONE}}
```

### Параметризація та fixtures

⭐ **Параметризований тест для всіх дозволених фігур.** `test_allowed_figure` виконується окремо для кожного типу з `Figure.FIGURES`. Тест `test_allowed_figure_length` поєднує два `parametrize`, тож перевіряється кожна комбінація типу й довжини (3 × 3 = 9 запусків). Для зрозумілих назв у виводі задано `ids` (square, rectangle, triangle).

⭐ **Fixture з довжиною 10.** Fixture `length` повертає 10, а `square_10` залежить від неї й створює квадрат. Тест `test_square_10_properties` перевіряє тип і довжину, а `test_length_fixture_dependency` показує, що залежна fixture отримує те саме значення.

🔥 **Тести для неправильних даних.** `test_invalid_figure_type` перевіряє кожен неправильний тип (`коло`, `ромб`, порожній рядок, `КВАДРАТ`), а `test_invalid_length_value` кожне неправильне значення довжини (0, -1, -100). У `pytest.raises` використано `match`, тому перевіряється й текст повідомлення, а не лише тип винятку.

### Розширені можливості

⭐ **Маркер `unit`.** Маркер додано до двох тестів (`test_triangle_type`, `test_square_length`) і зареєстровано в `pyproject.toml`. Запуск лише їх, `pytest -m unit -v`:

```text
{{CMD:UNIT}}
```

{{IMG:pictures/02_unit.png|Запуск тестів із маркером unit}}

⭐ **Fixture зі `scope="module"`.** У `conftest.py` fixture `allowed_figures` має область дії `module`, тобто pytest створює її один раз для модуля. Її використовують два тести: `test_allowed_figures_count` і `test_allowed_figures_content`. Оскільки fixture лежить у `conftest.py`, імпортувати її в тести не потрібно.

Команда `pytest --collect-only` показує всі знайдені тести без їх виконання:

```text
{{CMD:COLLECT}}
```

🔥 **Навмисно зламаний тест.** У `broken_examples/test_broken.py` тест `test_broken_length` очікує довжину 6 замість 5. Запуск `pytest broken_examples/test_broken.py -x --tb=short`:

```text
{{CMD:BROKEN}}
```

{{IMG:pictures/03_broken.png|Результат pytest -x --tb=short}}

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

Виконав усі завдання роботи, включно з ⭐ та 🔥: параметризовані тести для всіх фігур, fixtures (зокрема залежну та зі `scope="module"`), маркер `unit`, тести для кожного неправильного типу й значення довжини, навмисно зламаний тест із `-x --tb=short`. {{STATUS}}

Мети роботи досягнуто: навчився писати тести в pytest, використовувати `pytest.raises`, `parametrize`, fixtures, маркери та `conftest.py`.

Складності: pytest показує закодовані `\uXXXX` замість кирилиці в назвах параметризованих тестів, тому задав `ids` латиницею.

Feedback: формат здачі через посилання на репозиторій зручний, бо код, тести та звіт лежать разом.

Suggestions: додати в завдання приклад із `monkeypatch` або `capsys`, про які йдеться в описі.
