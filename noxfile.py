import nox


@nox.session
def tests(session):
    session.install('pytest')
    session.run('pytest tests/')


@nox.session
def lint(session):
    session.install('ruff')
    session.run('ruff', 'check', 'src/pyminideprecator/')
