import nox

PYPROJECT = nox.project.load_toml("pyproject.toml")
PYTHON_VERSIONS = nox.project.python_versions(PYPROJECT, max_version="3.14")


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    session.install(".", "--group", "tests")
    session.run("pytest", "--no-cov")
