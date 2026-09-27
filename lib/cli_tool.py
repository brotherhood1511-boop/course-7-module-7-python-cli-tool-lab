# cli_tool.py

import argparse
try:
    from lib.models import Task, User   # when run as: python -m lib.cli_tool (tests)
except ModuleNotFoundError:
    from models import Task, User       # when run as: python lib/cli_tool.py

# Global dictionary to store users and their tasks
users = {}


def add_task(args):
    user = users.get(args.user)
    if user is None:
        user = User(args.user)
        users[args.user] = user
    user.add_task(Task(args.title))


def complete_task(args):
    user = users.get(args.user)
    if user is None:
        print(f"❌ User '{args.user}' not found.")
        return
    task = user.get_task_by_title(args.title)
    if task is None:
        print(f"❌ Task '{args.title}' not found for {args.user}.")
        return
    task.complete()


# CLI entry point
def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers()

    # Subparser for adding tasks
    add_parser = subparsers.add_parser("add-task", help="Add a task for a user")
    add_parser.add_argument("user")
    add_parser.add_argument("title")
    add_parser.set_defaults(func=add_task)

    # Subparser for completing tasks
    complete_parser = subparsers.add_parser("complete-task", help="Complete a user's task")
    complete_parser.add_argument("user")
    complete_parser.add_argument("title")
    complete_parser.set_defaults(func=complete_task)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()