# Python-Project
A Python CLI tool for managing users, projects, and tasks using OOP and JSON persistence.



# Project Management CLI Tool (Python)

A beginner-friendly command-line application for managing **Users**, **Projects**, and **Tasks**.
Data is saved locally using **JSON file I/O**.

## Features
- Create and list users
- Add projects for a specific user
- List projects (optionally by user or search keyword)
- Add tasks to a project
- List tasks for a project
- Mark tasks as complete
- Local persistence using `data/db.json`
- Rich CLI tables using the `rich` package
- Basic unit tests included

## Tech Stack
- Python 3.10+
- argparse (CLI)
- JSON (persistence)
- rich (external package for better CLI output)

## Setup
1. Clone the repository:
   ```bash
   git clone <YOUR_REPO_URL>
   cd project-cli