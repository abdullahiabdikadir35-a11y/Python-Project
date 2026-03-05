from __future__ import annotations
from dataclasses import dataclass
from utils.validators import validate_title, validate_status


@dataclass
class Task:
    """
    Task model (many-to-many contributors in a simple way):
    - A task belongs to ONE project (project_id)
    - A task can have MULTIPLE contributors (list of user_ids)
    """

    id: int
    project_id: int
    _title: str
    _status: str = "pending"  # "pending" or "done"
    contributors: list[int] | None = None

    def __init__(
        self,
        task_id: int,
        project_id: int,
        title: str,
        status: str = "pending",
        contributors: list[int] | None = None,
    ) -> None:
        self.id = task_id
        self.project_id = project_id
        self.title = title
        self.status = status
        self.contributors = contributors or []

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = validate_title(value)

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = validate_status(value)

    def mark_done(self) -> None:
        self.status = "done"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "status": self.status,
            "contributors": self.contributors,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            task_id=data["id"],
            project_id=data["project_id"],
            title=data["title"],
            status=data.get("status", "pending"),
            contributors=data.get("contributors", []),
        )

    def __str__(self) -> str:
        return f"{self.title} (id={self.id}, status={self.status})"