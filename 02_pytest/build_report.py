import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).parent
ENV = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8", NO_COLOR="1")

COMMANDS = {
    "VERSION": ["--version"],
    "VERBOSE": ["-v"],
    "ONE": ["test_app.py::test_triangle_type", "-v"],
    "UNIT": ["-m", "unit", "-v"],
    "COLLECT": ["--collect-only"],
    "BROKEN": ["broken_examples/test_broken.py", "-x", "--tb=short"],
}


def run_pytest(args):
    result = subprocess.run(
        [sys.executable, "-m", "pytest", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=ENV,
    )
    return (result.stdout + result.stderr).strip()


def main():
    try:
        import pytest
    except ImportError:
        print("pytest не встановлено. Спочатку виконайте: py -m pip install pytest")
        sys.exit(1)

    outputs = {name: run_pytest(args) for name, args in COMMANDS.items()}

    verbose = outputs["VERBOSE"]
    summary = re.search(r"(\d+) passed", verbose)
    if summary and "failed" not in verbose and "error" not in verbose.lower().split("\n")[-1]:
        status = f"Усі {summary.group(1)} тестів проходять."
    else:
        status = "Не всі тести пройшли, див. вивід запуску вище."
        print("Увага: pytest -v завершився не повністю успішно. Перевірте вивід.")

    text = (ROOT / "README.template.md").read_text(encoding="utf-8")
    text = re.sub(r"\{\{CMD:(\w+)\}\}", lambda m: outputs[m.group(1)], text)
    text = re.sub(
        r"\{\{FILE:([^}]+)\}\}",
        lambda m: (ROOT / m.group(1)).read_text(encoding="utf-8").rstrip("\n"),
        text,
    )

    def image(match):
        path, alt = match.group(1).split("|")
        if (ROOT / path).exists():
            return f"![{alt}]({path})\n\n"
        return ""

    text = re.sub(r"\{\{IMG:([^}]+)\}\}\n?", image, text)
    text = text.replace("{{STATUS}}", status)
    text = re.sub(r"\n{3,}", "\n\n", text)
    (ROOT / "README.md").write_text(text, encoding="utf-8", newline="\n")
    print("README.md створено")


if __name__ == "__main__":
    main()
