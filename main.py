import argparse
import sys

from rich.console import Console
from rich.table import Table

from storage import JSONStore

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pm",
        description="Project Management CLI Tool (Users, Projects, Tasks)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # ---- users ----
    p_add_user = sub.add_parser("add-user", help="Create a new user")
    p_add_user.add_argument("--name", required=True, help="User name (example: Alex)")
    p_add_user.add_argument("--email", required=False, help="User email (optional)")

    p_list_users = sub.add_parser("list-users", help="List all users")

    # ---- projects ----
    p_add_project = sub.add_parser("add-project", help="Add a project to a user")
    p_add_project.add_argument("--user", required=True, help="User name who owns the project")
    p_add_project.add_argument("--title", required=True, help="Project title")
    p_add_project.add_argument("--description", required=False, help="Project description (optional)")
    p_add_project.add_argument("--due", required=False, help="Due date (YYYY-MM-DD) optional")

    p_list_projects = sub.add_parser("list-projects", help="List projects (all or by user)")
    p_list_projects.add_argument("--user", required=False, help="Filter by user name")
    p_list_projects.add_argument("--search", required=False, help="Search by project title keyword")

    p_set_due = sub.add_parser("set-project-due", help="Update a project's due date")
    p_set_due.add_argument("--project", required=True, help="Project title")
    p_set_due.add_argument("--due", required=False, help="Due date (YYYY-MM-DD). Use empty to clear.", default=None)

    # ---- tasks ----
    p_add_task = sub.add_parser("add-task", help="Add a task to a project")
    p_add_task.add_argument("--project", required=True, help="Project title")
    p_add_task.add_argument("--title", required=True, help="Task title")
    p_add_task.add_argument(
        "--contributors",
        nargs="*",
        required=False,
        help="Optional list of contributor user names (example: --contributors Alex Sam)",
    )

    p_list_tasks = sub.add_parser("list-tasks", help="List tasks for a project")
    p_list_tasks.add_argument("--project", required=True, help="Project title")

    p_done = sub.add_parser("complete-task", help="Mark a task as complete")
    p_done.add_argument("--id", type=int, required=True, help="Task ID (number)")

    return parser


def print_users(users) -> None:
    table = Table(title="Users")
    table.add_column("ID", justify="right")
    table.add_column("Name")
    table.add_column("Email")

    for u in users:
        table.add_row(str(u.id), u.name, u.email or "-")
    console.print(table)


def print_projects(projects, store: JSONStore) -> None:
    table = Table(title="Projects")
    table.add_column("ID", justify="right")
    table.add_column("Title")
    table.add_column("Owner")
    table.add_column("Due Date")
    table.add_column("Description")

    for p in projects:
        owner = store.get_user_by_id(p.user_id)
        owner_name = owner.name if owner else "Unknown"
        table.add_row(str(p.id), p.title, owner_name, p.due_date or "-", p.description or "-")
    console.print(table)


def print_tasks(tasks, store: JSONStore) -> None:
    table = Table(title="Tasks")
    table.add_column("ID", justify="right")
    table.add_column("Title")
    table.add_column("Status")
    table.add_column("Contributors")

    for t in tasks:
        contributor_names = []
        for uid in t.contributors:
            u = store.get_user_by_id(uid)
            contributor_names.append(u.name if u else f"id:{uid}")
        table.add_row(str(t.id), t.title, t.status, ", ".join(contributor_names) if contributor_names else "-")

    console.print(table)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    store = JSONStore("data/db.json")

    try:
        if args.command == "add-user":
            user = store.add_user(name=args.name, email=args.email)
            console.print(f"[green]Created user:[/green] {user}")

        elif args.command == "list-users":
            users = store.list_users()
            print_users(users)

        elif args.command == "add-project":
            project = store.add_project(
                user_name=args.user,
                title=args.title,
                description=args.description,
                due_date=args.due,
            )
            console.print(f"[green]Created project:[/green] {project} for user '{args.user}'")

        elif args.command == "list-projects":
            projects = store.list_projects(user_name=args.user, search=args.search)
            print_projects(projects, store)

        elif args.command == "set-project-due":
            # If they pass an empty string, treat it as clearing the due date
            due = args.due
            if isinstance(due, str) and due.strip() == "":
                due = None
            project = store.update_project_due_date(project_title=args.project, due_date=due)
            console.print(f"[green]Updated project due date:[/green] {project.title} -> {project.due_date or 'cleared'}")

        elif args.command == "add-task":
            task = store.add_task(project_title=args.project, title=args.title, contributors=args.contributors)
            console.print(f"[green]Created task:[/green] {task}")

        elif args.command == "list-tasks":
            tasks = store.list_tasks(project_title=args.project)
            print_tasks(tasks, store)

        elif args.command == "complete-task":
            task = store.complete_task(task_id=args.id)
            console.print(f"[green]Task completed:[/green] {task}")

        else:
            parser.print_help()
            return 1

        return 0

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())