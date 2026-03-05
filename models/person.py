class Person:
    """
    Base class to demonstrate inheritance.
    A User is a Person with extra behavior/requirements.
    """

    def __init__(self, name: str, email: str | None = None) -> None:
        self.name = name
        self.email = email

    def __repr__(self) -> str:
        return f"Person(name={self.name!r}, email={self.email!r})"