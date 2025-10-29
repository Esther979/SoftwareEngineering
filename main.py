import shlex
from datetime import datetime
from typing import List, Dict, Callable

from src.app import Employee, Role, Manager, Worker, Department, TaskStatus, WorkflowSystem, EventApplicationStatus

# ---------------------------------------------------------------------
# Mock database
# ---------------------------------------------------------------------
USERS: Dict[str, Employee] = {
    "mike@sep.se": Employee("Mike", Role.ADM_MANAGER),

    "alice@sep.se": Employee("Alice", Role.FIN_MANAGER),

    "janet@sep.se": Employee("Janet", Role.CS_MANAGER),
    "sarah@sep.se": Employee("Sarah", Role.CS_WORKER),

    "jack@sep.se": Manager("Jack", Department.PRODUCTION),
    "tobias@sep.se": Worker("Tobias", Department.PRODUCTION, "Photographer"),
    "antony@sep.se": Worker("Antony", Department.PRODUCTION, "Audio Specialist"),

    "natalie@sep.se": Manager("Natalie", Department.SERVICES),
    "helen@sep.se": Worker("Helen", Department.SERVICES, "Top Chef"),
    "diana@sep.se": Worker("Diana", Department.SERVICES, "Chef"),
    "kate@sep.se": Worker("Kate", Department.SERVICES, "Top Waiter"),
    "lauren@sep.se": Worker("Lauren", Department.SERVICES, "Waiter"),
}

# ---------------------------------------------------------------------
# Global state
# ---------------------------------------------------------------------
CURRENT_USER: Employee | None = None
SYSTEM = WorkflowSystem()

# ---------------------------------------------------------------------
# Decorators
# ---------------------------------------------------------------------
def require_login(func: Callable):
    """Decorator to ensure a user is logged in."""
    def wrapper(*args, **kwargs):
        if CURRENT_USER is None:
            print("⚠️  You must log in first.")
            return
        return func(*args, **kwargs)
    return wrapper

def require_role(*roles: Role):
    """Decorator to restrict access to certain roles."""
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            if CURRENT_USER is None:
                print("⚠️  You must log in first.")
                return
            if CURRENT_USER.role not in roles:
                print(f"🚫 Permission denied for {CURRENT_USER.role.value}.")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator

# ---------------------------------------------------------------------
# Help function
# ---------------------------------------------------------------------
def show_help(role: Role | None = None):
    print("")
    if role is None:
        print("Available commands:")
        print("  login <email>                      Log in")
        print("  help                               Show this help")
        print("  quit                               Exit the program")
        return

    print("Available commands:")
    match role:
        case Role.MANAGER:
            print("  create-task <event-id> <title> <desc>  Create a new task")
            print("  assign-task <title> <emails...>        Assign a task to workers")
            print("  update-task-status <title> <status>    Change task status (Open/In_Progress/Closed)")           
            print("  view-tasks                             View your created tasks")
            print("  review-task <title>                    Review feedback and budget requests")
        case Role.WORKER:
            print("  view-tasks                             View your assigned tasks")
            print("  comment-on-task <title> <text>         Add a comment to a task")

        case Role.CS_WORKER:
            print("  create-event-application <client> <event_type> <start> <end> <budget> [preferences]")
            print("  view-event-application <app_id>")
        case Role.FIN_MANAGER | Role.ADM_MANAGER:
            print("  view-event-application <app_id>")
            print("  review-event-application <app_id> <FORWARDED|APPROVED|REJECTED> <comment>")
        case _:
            print("  (No specific actions for this role)")
    print("  logout                                 Log out")
    print("  quit                                   Exit program")
    print("")

# ---------------------------------------------------------------------
# Command functions
# ---------------------------------------------------------------------
@require_role(Role.CS_WORKER)
def create_event_application(args: list[str]):
    if len(args) < 5:
        print("Usage: create-event-application <client> <event_type> <start> <end> <budget> [preferences]")
        return
    client, event_type, start_str, end_str, budget_str, *prefs = args
    try:
        start = datetime.fromisoformat(start_str)
        end = datetime.fromisoformat(end_str)
        budget = float(budget_str)
    except Exception as e:
        print(f"❌ Invalid date or budget: {e}")
        return
    preferences = " ".join(prefs)
    app = SYSTEM.create_event_application(
        client_name=client,
        event_type=event_type,
        start_date=start,
        end_date=end,
        budget=budget,
        preferences=preferences
        created_by=CURRENT_USER.role
    )
    print(f"🆕 Created Event Application #{app.app_id} for {client}")


@require_role(Role.CS_WORKER, Role.FIN_MANAGER, Role.ADM_MANAGER)
def view_event_application(args: list[str]):
    if not args:
        print("Usage: view-event-application <app_id>")
        return
    try:
        app_id = int(args[0])
        app = SYSTEM.get_application_by_id(app_id)
        print(f"[#{app.app_id}] {app.client_name} - {app.event_type}")
        print(f"Status: {app.status.value}")
        print(f"Budget: {app.budget}")
        print(f"Preferences: {app.preferences}")
        print(f"Created by: {app.created_by.value}")
        print("History:")
        for entry in app.history:
            timestamp, role, action, comment = entry
            print(f"  {timestamp} | {role.value} | {action} | {comment}")
        if app.comment:
            print(f"Comment: {app.comment}")
    except Exception as e:
        print(f"❌ {e}")


@require_role(Role.FIN_MANAGER, Role.ADM_MANAGER)
def review_event_application(args: list[str]):
    if len(args) < 3:
        print("Usage: review-event-application <app_id> <FORWARDED|APPROVED|REJECTED> <comment>")
        return
    try:
        app_id = int(args[0])
        decision_str = args[1].upper()
        comment = " ".join(args[2:])
        decision = EventApplicationStatus[decision_str]
        SYSTEM.review_application(app_id, CURRENT_USER.role, decision, comment)
        print(f"✅ Application #{app_id} updated to {decision.value}")
    except KeyError:
        print("❌ Invalid decision. Choose: FORWARDED, APPROVED, REJECTED")
    except Exception as e:
        print(f"❌ {e}")

@require_role(Role.MANAGER)
def create_task(args: List[str]):
    if len(args) < 3:
        print("Usage: create-task <event-id> <title> <description>")
        return
    
    try:
        event_id = int(args[0])
    except ValueError:
        print("❌ Event ID must be a number.")
        return

    try:
        event = SYSTEM.get_application_by_id(event_id)
    except ValueError:
        print(f"❌ No event found with ID {event_id}.")
        return

    title = args[1]
    description = " ".join(args[2:])

    manager: Manager = CURRENT_USER
    task = manager.create_task(event_id, title, description)
    print(f"🆕 Created task '{task.title}' linked to Event #{task.event_id} ({event.client_name}) ({task.department.value} Department)")

@require_role(Role.MANAGER)
def assign_task(args: list[str]):
    if len(args) < 2:
        print("Usage: assign-task <task-title> <worker_emails...>")
        return
    title, emails = args[0], args[1:]
    manager: Manager = CURRENT_USER
    task = next((t for t in manager.tasks if t.title == title), None)
    if not task:
        print("❌ Task not found.")
        return
    workers: List[Worker] = []
    for e in emails:
        w = USERS.get(e)
        if isinstance(w, Worker):
            workers.append(w)
    if not workers:
        print("No valid workers found.")
        return
    manager.assign_task(task, workers)
    print(f"✅ Assigned '{title}' to {', '.join(w.name for w in workers)}")


@require_login
@require_role(Role.MANAGER, Role.WORKER)
def view_tasks(_: list[str]):
    if isinstance(CURRENT_USER, (Manager, Worker)):
        tasks = CURRENT_USER.view_tasks()
        if not tasks:
            print("No tasks found.")
            return
        for t in tasks:
            print(f"- {t.title} ({t.status.value})")
    else:
        print("Your role has no tasks.")


@require_role(Role.WORKER)
def comment_on_task(args: list[str]):
    if len(args) < 2:
        print("Usage: comment-on-task <task-title> <comment>")
        return
    title, comment_text = args[0], " ".join(args[1:])
    worker: Worker = CURRENT_USER  # type: ignore
    task = next((t for t in worker.tasks if t.title == title), None)
    if not task:
        print("❌ Task not found.")
        return
    worker.comment_on_task(task, comment_text)
    print("💬 Comment added.")


@require_role(Role.MANAGER)
def update_task_status(args: list[str]):
    if len(args) < 2:
        print("Usage: update-task-status <task-title> <Open|In_Progress|Closed>")
        return
    title, status_str = args[0], args[1]
    manager: Manager = CURRENT_USER  # type: ignore
    task = next((t for t in manager.tasks if t.title == title), None)
    if not task:
        print("❌ Task not found.")
        return
    try:
        new_status = TaskStatus[status_str.upper()]
    except KeyError:
        print("❌ Invalid status. Use: Open, In_Progress, Closed.")
        return
    manager.change_task_status(task, new_status)
    print(f"🔄 Task '{title}' updated to {new_status.value}")

@require_role(Role.MANAGER)
def review_task(args: list[str]):
    if len(args) < 1:
        print("Usage: review-task <task-title>")
        return

    title = " ".join(args)
    manager: Manager = CURRENT_USER  # type: ignore

    # Find task by title
    task = next((t for t in manager.tasks if t.title == title), None)
    if not task:
        print(f"❌ No task found with title '{title}'.")
        return

    # --- Comments ---
    comments = manager.review_feedback(task)
    if comments:
        print(f"\n💬 Comments for '{task.title}':")
        for c in comments:
            ts = c['timestamp'].strftime("%Y-%m-%d %H:%M")
            print(f"  - [{ts}] {c['worker']}: {c['comment']}")
    else:
        print("\n💬 No comments yet.")

    # --- Budget Requests ---
    budgets = manager.review_budget_requests(task)
    if budgets:
        print(f"\n💰 Budget Requests for '{task.title}':")
        for b in budgets:
            ts = b['timestamp'].strftime("%Y-%m-%d %H:%M")
            print(f"  - [{ts}] {b['worker']} requested {b['amount']} SEK — {b['reason']}")
    else:
        print("\n💰 No budget requests yet.")

def cli():
    global CURRENT_USER

    print("\nSEP Internal System CLI ⚙️")
    print("Type 'help' to see available commands.\n")

    while True:
        prompt = f"[{CURRENT_USER.name}] > " if CURRENT_USER else "> "
        try:
            raw = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not raw:
            continue

        parts = shlex.split(raw)
        cmd, args = parts[0].lower(), parts[1:]

        # Pre-authentication.
        if CURRENT_USER is None:
            match cmd:
                case "help" | "?":
                    show_help(None)
                    continue

                case "quit" | "exit":
                    print("👋 Goodbye!")
                    break

                case "login":
                    if not args:
                        email = input("Enter your email to login: ")
                    else:
                        email = args[0]

                    CURRENT_USER = USERS.get(email)
                    if not CURRENT_USER:
                        print("❌ User not found.\n")
                        continue

                    print(f"✅ Logged in as {CURRENT_USER.name} ({CURRENT_USER.__class__.__name__}, {CURRENT_USER.role.value})\n")
                    continue

                case _:
                    print("❓ Unknown command. Type 'help' for options.")
                    continue
        
        # Post-authentication.
        match cmd:
            case "help" | "?":
                show_help(CURRENT_USER.role)
                continue

            case "logout":
                print("👋 Logged out\n")
                CURRENT_USER = None
                continue
            
            case "quit" | "exit":
                print("👋 Goodbye!\n")
                break

            case "create-event-application": create_event_application(args)
            case "view-event-application": view_event_application(args)
            case "review-event-application": review_event_application(args)
            case "create-task": create_task(args)
            case "assign-task": assign_task(args)
            case "view-tasks": view_tasks(args)
            case "comment-on-task": comment_on_task(args)
            case "update-task-status": update_task_status(args)
            case "review-task": review_task(args)

            case _:
                print("❓ Unknown command. Type 'help' for options.")
                continue
                

def main():
    cli()

if __name__ == "__main__":
    main()