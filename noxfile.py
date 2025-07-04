import nox

# uv will handle any missing python versions
python_versions = ["3.10", "3.11", "3.12", "3.13"]


@nox.session(python=python_versions, venv_backend='uv')
def tests(session):
    """Run tests on specified Python versions."""
    # Install the package and test dependencies with uv
    session.run_always("uv", "pip", "install", ".", external=True)

    session.install(
        "pytest-xdist",
        "pytest-randomly",
        "pytest-sugar",
    )

    # Run pytest with common options
    session.run(
        "pytest",
        "tests/",
        "-v",                   # verbose output
        "-s",                   # don't capture output
        "--tb=short",           # shorter traceback format
        "--strict-markers",     # treat unregistered markers as errors
        "-n", "auto",           # parallel testing
        *session.posargs        # allows passing additional pytest args from command line
    )


@nox.session
def lint(session):
    session.install('ruff')
    session.run('ruff', 'check', 'src/pyminideprecator/')

