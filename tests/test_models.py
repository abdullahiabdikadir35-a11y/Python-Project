import unittest

from models import User, Project, Task


class TestModels(unittest.TestCase):
    def test_user_validation(self):
        u = User(user_id=1, name="Alex", email="alex@example.com")
        self.assertEqual(u.name, "Alex")
        self.assertEqual(u.email, "alex@example.com")

        with self.assertRaises(ValueError):
            User(user_id=2, name="A")  # too short

    def test_project_due_date_validation(self):
        p = Project(project_id=1, user_id=1, title="CLI Tool", due_date="2026-03-20")
        self.assertEqual(p.due_date, "2026-03-20")

        with self.assertRaises(ValueError):
            Project(project_id=2, user_id=1, title="Bad Date", due_date="20-03-2026")

    def test_task_done(self):
        t = Task(task_id=1, project_id=1, title="Write code")
        self.assertEqual(t.status, "pending")
        t.mark_done()
        self.assertEqual(t.status, "done")


if __name__ == "__main__":
    unittest.main()