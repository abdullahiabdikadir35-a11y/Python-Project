import re
from datetime import datetime


def validate_name(name: str) -> str:
    name = (name or "").strip()
    if len(name) < 2:
        raise ValueError("Name must be at least 2 characters.")
    return name


def validate_title(title: str) -> str:
    title = (title or "").strip()
    if len(title) < 2:
        raise ValueError("Title must be at least 2 characters.")
    return title


def validate_optional_text(text: str | None) -> str | None:
    if text is None:
        return None
    text = text.strip()
    return text if text else None


def validate_email_optional(email: str | None) -> str | None:
    if email is None:
        return None
    email = email.strip()
    if not email:
        return None

    # Simple beginner-friendly email validation
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(pattern, email):
        raise ValueError("Invalid email format. Example: alex@gmail.com")
    return email


def validate_due_date_optional(due_date: str | None) -> str | None:
    """
    Accepts YYYY-MM-DD or None.
    """
    if due_date is None:
        return None
    due_date = due_date.strip()
    if not due_date:
        return None
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("due_date must be in YYYY-MM-DD format (example: 2026-03-20).")
    return due_date


def validate_status(status: str) -> str:
    status = (status or "").strip().lower()
    if status not in {"pending", "done"}:
        raise ValueError("Status must be either 'pending' or 'done'.")
    return status