import json
import os
from typing import Any

from models import User, Project, Task


class JSONStore:
    """
    Handles reading/writing to a local JSON file.

    Structure inside db.json:
    {
      "counters": {"users": 0, "projects": 0, "tasks": 0},
      "users": [],
      "projects": [],
      "tasks": []
    }
    """

    def __init__(self, path: str) -> None:
        self.path = path
        self._ensure_file()

    def _ensure_file(self) -> None:
        # Create folders if missing
        folder = os.path.dirname(self.path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        # Create file if missing or empty
        if not os.path.exists(self.path) or os.path.getsize(self.path) == 0:
            self._write_data(
                {"counters": {"users": 0, "projects": 0, "tasks": 0},
                 "users": [], "projects": [], "tasks": []}
            )
        else:
            # If file exists but is {} or malformed, try to fix safely
            try:
                data = self._read_data()
                if "users" not in data:
                    self._write_data(
                        {"counters": {"users": 0, "projects": 0, "tasks": 0},
                         "users": [], "projects": [], "tasks": []}
                    )
            except Exception:
                self._write_data(
                    {"counters": {"users": 0, "projects": 0, "tasks": 0},
                     "users": [], "projects": [], "tasks": []}
                )

    def _read_data(self) -> dict[str, Any]:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_data(self, data: dict[str, Any]) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # ---------- ID counters ----------
    def _next_id(self, key: str) -> int:
        data = self._read_data()
        data["counters"][key] += 1
        new_id = data["counters"][key]
        self._write_data(data)
        return new_id

    # ---------- Users ----------
    def add_user(self, name: str, email: str | None = None) -> User:
        data = self._read_data()

        # Prevent duplicate user names (simple rule)
        if any(u["name"].lower() == name.strip().lower() for u in data["users"]):
            raise ValueError(f"User with name '{name}' already exists.")

        user_id = self._next_id("users")
        user = User(user_id=user_id, name=name, email=email)

        data = self._read_data()
        data["users"].append(user.to_dict())
        self._write_data(data)
        return user

    def list_users(self) -> list[User]:
        data = self._read_data()
        return [User.from_dict(u) for u in data["users"]]

    def get_user_by_name(self, name: str) -> User | None:
        data = self._read_data()
        for u in data["users"]:
            if u["name"].lower() == name.strip().lower():
                return User.from_dict(u)
        return None

    def get_user_by_id(self, user_id: int) -> User | None:
        data = self._read_data()
        for u in data["users"]:
            if u["id"] == user_id:
                return User.from_dict(u)
        return None

    # ---------- Projects ----------
    def add_project(
        self,
        user_name: str,
        title: str,
        description: str | None = None,
        due_date: str | None = None,
    ) -> Project:
        user = self.get_user_by_name(user_name)
        if not user:
            raise ValueError(f"User '{user_name}' not found. Create them first.")

        project_id = self._next_id("projects")
        project = Project(
            project_id=project_id,
            user_id=user.id,
            title=title,
            description=description,
            due_date=due_date,
        )

        data = self._read_data()
        data["projects"].append(project.to_dict())
        self._write_data(data)
        return project

    def list_projects(self, user_name: str | None = None, search: str | None = None) -> list[Project]:
        data = self._read_data()
        projects = [Project.from_dict(p) for p in data["projects"]]

        if user_name:
            user = self.get_user_by_name(user_name)
            if not user:
                return []
            projects = [p for p in projects if p.user_id == user.id]

        if search:
            s = search.strip().lower()
            projects = [p for p in projects if s in p.title.lower()]

        return projects

    def get_project_by_title(self, title: str) -> Project | None:
        data = self._read_data()
        for p in data["projects"]:
            if p["title"].lower() == title.strip().lower():
                return Project.from_dict(p)
        return None

    def update_project_due_date(self, project_title: str, due_date: str | None) -> Project:
        data = self._read_data()
        for i, p in enumerate(data["projects"]):
            if p["title"].lower() == project_title.strip().lower():
                proj = Project.from_dict(p)
                proj.due_date = due_date
                data["projects"][i] = proj.to_dict()
                self._write_data(data)
                return proj
        raise ValueError(f"Project '{project_title}' not found.")

    # ---------- Tasks ----------
    def add_task(self, project_title: str, title: str, contributors: list[str] | None = None) -> Task:
        project = self.get_project_by_title(project_title)
        if not project:
            raise ValueError(f"Project '{project_title}' not found.")

        contributor_ids: list[int] = []
        if contributors:
            for name in contributors:
                user = self.get_user_by_name(name)
                if not user:
                    raise ValueError(f"Contributor '{name}' not found. Create user first.")
                contributor_ids.append(user.id)

        task_id = self._next_id("tasks")
        task = Task(task_id=task_id, project_id=project.id, title=title, contributors=contributor_ids)

        data = self._read_data()
        data["tasks"].append(task.to_dict())
        self._write_data(data)
        return task

    def list_tasks(self, project_title: str) -> list[Task]:
        project = self.get_project_by_title(project_title)
        if not project:
            raise ValueError(f"Project '{project_title}' not found.")

        data = self._read_data()
        tasks = [Task.from_dict(t) for t in data["tasks"] if t["project_id"] == project.id]
        return tasks

    def complete_task(self, task_id: int) -> Task:
        data = self._read_data()
        for i, t in enumerate(data["tasks"]):
            if t["id"] == task_id:
                task = Task.from_dict(t)
                task.mark_done()
                data["tasks"][i] = task.to_dict()
                self._write_data(data)
                return task
        raise ValueError(f"Task id={task_id} not found.")