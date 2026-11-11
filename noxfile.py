#!/usr/bin/env -S uv run --script --quiet

# /// script
# dependencies = ["nox[uv]"]
# ///

from __future__ import annotations

from pathlib import Path

import nox

PYTHON_VERSIONS = [
    # "3.11",
    # "3.12",
    # "3.13",
    "3.14"
]
DEFAULT_PYTHON = max(PYTHON_VERSIONS)

repo_root = Path(__file__).parent

reports_root = repo_root / "build/report"
src_root = repo_root / "src"
docs_root = repo_root / "docs"

nox.options.default_venv_backend = "uv"


@nox.session(python=DEFAULT_PYTHON)
def lint(session: nox.Session):
    session.install("ruff")
    session.run("ruff", "check", "--fix", "--unsafe-fixes", "src", "test")


@nox.session(python=DEFAULT_PYTHON)
def format_doc(session: nox.Session):
    session.install("docstrfmt")
    session.run("docstrfmt")


@nox.session(python=PYTHON_VERSIONS)
def pytest(session: nox.Session):
    session.run_install(
        "uv",
        "sync",
        f"--python={session.virtualenv.location}",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run(*_coverage_cmd(session.name, ["pytest", "test"]))


@nox.session(python=PYTHON_VERSIONS, default=False)
def typing(session: nox.Session):
    session.run_install(
        "uv",
        "sync",
        f"--python={session.virtualenv.location}",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run("mypy", "--python-version", session.python, "src")


@nox.session(python=DEFAULT_PYTHON)
def coverage(session: nox.Session):
    session.run_install(
        "uv",
        "sync",
        f"--python={session.virtualenv.location}",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    session.run("coverage", "combine", "--keep")
    session.run("coverage", "xml")
    session.run("coverage", "html")
    session.run("coverage", "report")

    html_report = reports_root / "coverage/html/index.html"
    xml_report = reports_root / "coverage.xml"

    session.log(f"Cobertura-compatible test coverage report at {xml_report.resolve()}")
    session.log(f"Browse HTML test coverage report at {html_report.resolve()}")


@nox.session(python=DEFAULT_PYTHON)
def docs(session: nox.Session):
    session.run_install(
        "uv",
        "sync",
        f"--python={session.virtualenv.location}",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    # session.run(*_python_cmd(_sphinx_apidoc_modulecmd()))
    session.run(*_python_cmd(_sphinx_build_modulecmd()))


def _sphinx_apidoc_modulecmd() -> list[str]:
    return [
        "sphinx.ext.apidoc",
        "-o",
        "docs/apidoc",
        "--force",
        "--no-toc",
        "--separate",
        "--module-first",
        "src",
    ]


def _sphinx_build_modulecmd(
    build_root: str = "build", session_name: str = "sphinx", builder: str = "html"
) -> list[str]:
    return [
        "sphinx",
        "-b",
        builder,
        "-d",
        f"{build_root}/{session_name}/doctrees",
        "-E",
        "-n",
        "-W",
        "--keep-going",
        "-T",
        "docs",
        f"{build_root}/{session_name}/{builder}",
    ]


def _python_cmd(modulecmd: list[str]) -> list[str]:
    return ["python", "-m", *modulecmd]


def _coverage_cmd(context: str, modulecmd: list[str]) -> list[str]:
    return [
        "python",
        "-m",
        "coverage",
        "run",
        f"--context={context}",
        "-m",
        *modulecmd,
    ]


if __name__ == "__main__":
    nox.main()
