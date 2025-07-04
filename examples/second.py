from pyminideprecator import deprecate, set_current_version

set_current_version("0.5.0")


@deprecate(
    remove_version="2024.01.01",
    message="Old database client",
    instead="NewDBClient",
    category=FutureWarning,
)
class OldDBClient:
    def __init__(self, url: str):
        self.url = url

    def query(self, sql: str) -> list:
        return ["result1", "result2"]


client = OldDBClient("db://localhost")  # Выдает FutureWarning
print(client.query("SELECT * FROM table"))
