from pyminideprecator import deprecate, set_current_version

set_current_version('0.1.0')


@deprecate(
    remove_version='1.1.1',
    message='Old database client',
    instead='NewDBClient',
    category=FutureWarning,
)
class OldDBClient:
    def __init__(self, url: str):
        self.url = url

    def query(self, sql: str) -> list:
        return ['result1', 'result2']


client = OldDBClient('db://localhost')
print(client.query('SELECT * FROM table'))
