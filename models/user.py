from __future__ import annotations
from dataclasses import dataclass

from .person import Person
from utils.validators import validate_name, validate_email_optional


@dataclass
class User(Person):
    """
    User model.
    - Uses inheritance: User(Person)
    - Demonstrates properties/setters for validation
    """

    id: int
    _name: str
    _email: str | None = None

    def __init__(self, user_id: int, name: str, email: str | None = None) -> None:
        # Call Person init (inheritance)
        super().__init__(name=name, email=email)

        self.id = user_id
        self.name = name
        self.email = email

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = validate_name(value)

    @property
    def email(self) -> str | None:
        return self._email

    @email.setter
    def email(self, value: str | None) -> None:
        self._email = validate_email_optional(value)

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(user_id=data["id"], name=data["name"], email=data.get("email"))

    def __str__(self) -> str:
        return f"{self.name} (id={self.id})"