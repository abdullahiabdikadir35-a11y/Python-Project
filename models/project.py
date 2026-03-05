from __future__ import annotations
from dataclasses import dataclass
from utils.validators import validate_title, validate_optional_text, validate_due_date_optional


@dataclass
class Project:
    """
    Project model (one-to-many with tasks):
    - A project has many tasks (stored separately in JSON, linked by project_id)
    """

    id: int
    user_id: int
    _title: str
    _description: str | None = None
    _due_date: str | None = None  # keep as string for simplicity (YYYY-MM-DD)

    def __init__(
        self,
        project_id: int,
        user_id: int,
        title: str,
        description: str | None = None,
        due_date: str | None = None,
    ) -> None:
        self.id = project_id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.due_date = due_date

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = validate_title(value)

    @property
    def description(self) -> str | None:
        return self._description

    @description.setter
    def description(self, value: str | None) -> None:
        self._description = validate_optional_text(value)

    @property
    def due_date(self) -> str | None:
        return self._due_date

    @due_date.setter
    def due_date(self, value: str | None) -> None:
        self._due_date = validate_due_date_optional(value)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        return cls(
            project_id=data["id"],
            user_id=data["user_id"],
            title=data["title"],
            description=data.get("description"),
            due_date=data.get("due_date"),
        )

    def __str__(self) -> str:
        return f"{self.title} (id={self.id})"