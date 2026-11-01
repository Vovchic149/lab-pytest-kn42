.PHONY: install test unit collect broken report clean

install:
	poetry install

test:
	poetry run pytest -v

unit:
	poetry run pytest -m unit -v

collect:
	poetry run pytest --collect-only

broken:
	poetry run pytest broken_examples/test_broken.py -x --tb=short

report:
	py build_report.py

clean:
	rm -rf .pytest_cache __pycache__
