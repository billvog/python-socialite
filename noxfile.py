import nox  # type: ignore
from pathlib import Path

nox.options.sessions = ["tests", "lint", "build"]

python = ["3.8"]


lint_dependencies = [
    "-e",
    ".",
    "black",
    "flake8",
    "flake8-bugbear",
    "mypy",
    "check-manifest",
    "codacy-coverage",
]


@nox.session(python=python)
def tests(session):
    session.install("-e", ".", "pytest", "pytest-cov")
    tests = session.posargs or ["tests"]
    session.run(
        "pytest",
        "--cov=python_socialite",
        "--cov-config",
        ".coveragerc",
        "--cov-report=xml",
        *tests
    )
    session.notify("cover")


@nox.session
def cover(session):
    """Coverage analysis."""
    session.install("coverage")
    session.run("coverage", "report", "--show-missing", "--fail-under=90")
    session.run("coverage", "erase")


@nox.session
def coverage_upload(session):
    """Upload coverage report to codacy."""
    session.install("codacy-coverage")
    session.run("python-codacy-coverage", "-r", "coverage.xml")


@nox.session(python="3.8")
def lint(session):
    session.install(*lint_dependencies)
    files = ["tests"] + [str(p) for p in Path(".").glob("*.py")]
    files.remove("manual_test.py")
    session.run("black", "--check", *files)
    session.run("flake8", *files)
    session.run("mypy", "--ignore-missing", *files)
    session.run("python", "setup.py", "check", "--metadata", "--strict")
    if "--skip_manifest_check" in session.posargs:
        pass
    else:
        session.run("check-manifest")


@nox.session(python="3.8")
def build(session):
    session.install("setuptools")
    session.install("wheel")
    session.install("twine")
    session.run("rm", "-rf", "dist", "build", external=True)
    session.run("python", "setup.py", "--quiet", "sdist", "bdist_wheel")


@nox.session(python="3.8")
def publish(session):
    build(session)
    print("REMINDER: Has the changelog been updated?")
    session.run("python", "-m", "twine", "upload", "dist/*")
