import shlex
from datetime import datetime
from typing import List, Dict, Callable

from src import Employee, Role, Manager, Worker, Department, TaskStatus, EventSystem, EventApplicationStatus, HRRequest, BudgetRequest, BudgetNegotiation

# ---------------------------------------------------------------------
# Mock database
# ---------------------------------------------------------------------
USERS: Dict[str, Employee] = {
    "mike@sep.se": Employee("Mike", Role.ADM_MANAGER),

    "alice@sep.se": Employee("Alice", Role.FIN_MANAGER),

    "janet@sep.se": Employee("Janet", Role.CS_MANAGER),
    "sarah@sep.se": Employee("Sarah", Role.CS_WORKER),

    "simon@sep.se": Employee("Simon", Role.HR_MANAGER),
    "maria@sep.se": Employee("Maria", Role.HR_WORKER),

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
SYSTEM = EventSystem()

HR_REQUESTS: Dict[int, HRRequest] = {}
BUDGET_REQUESTS: Dict[int, BudgetRequest] = {}
BUDGET_NEGOTIATIONS: Dict[int, BudgetNegotiation] = {}

next_hr_id = 1
next_budget_id = 1
next_negotiation_id = 1

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
        print("")
        return

    print("Available commands:")
    match role:
        case Role.MANAGER:
            print("  create-task <event-id> <title> <desc>    Create a new task")
            print("  assign-task <title> <emails...>          Assign a task to workers")
            print("  update-task-status <title> <status>      Change task status (Open/In_Progress/Closed)")           
            print("  view-tasks                               View your created tasks")
            print("  review-task <title>                      Review feedback and budget requests")
            print("  create-hr-request <type>                 Create a HR request")
            print("  create-budget-request <event-id> <amount> <reason>")
            print("  view-budget-requests                     View your department’s budget requests")

        case Role.WORKER:
            print("  view-tasks                               View your assigned tasks")
            print("  comment-on-task <title> <text>           Add a comment to a task")

        case Role.HR_MANAGER:
            print("  view-hr-requests                         View all HR requests")
            print("  review-hr-request <id> <approve|reject>  Approve or reject HR requests")

        case Role.HR_WORKER:
            print("  create-hr-request <type>                 Create a new HR request")
            print("  view-hr-requests                         View all HR requests")
            print("  hire-staff <id> <email> <name> <department> <duty>  Hire a new staff member for an approved request")

        case Role.CS_MANAGER:
            print("  review-event-application <app_id> FORWARDED <comment>   Forward an event application to Financial Manager")
            print("  view-event-application <app_id>")

        case Role.CS_WORKER:
            print("  create-event-application <client> <event_type> <start> <end> <budget> [preferences]")
            print("  view-event-application <app_id>")

        case Role.FIN_MANAGER:
            print("  view-event-application <app_id>")
            print("  review-event-application <app_id> <FORWARDED|APPROVED|REJECTED> <comment>")
            print("  review-budget-request <id> <approve|reject>")
            print("  negotiate-budget <id> <new-amount>")
            print("  view-budget-requests                     View all budget requests")

        case Role.ADM_MANAGER:
            print("  view-event-application <app_id>")
            print("  review-event-application <app_id> <FORWARDED|APPROVED|REJECTED> <comment>")

        case _:
            print("  (No specific actions for this role)")

    print("  logout                                  Log out")
    print("  quit                                    Exit program")
    print("")


# ---------------------------------------------------------------------
# Command functions
# ---------------------------------------------------------------------
@require_role(Role.CS_WORKER)
def create_event_application(args: List[str]):
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
        preferences=preferences,
        created_by=CURRENT_USER.role
    )
    print(f"🆕 Created Event Application #{app.app_id} for {client}")


@require_role(Role.CS_WORKER, Role.FIN_MANAGER, Role.ADM_MANAGER)
def view_event_application(args: List[str]):
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


@require_role(Role.CS_MANAGER, Role.FIN_MANAGER, Role.ADM_MANAGER)
def review_event_application(args: List[str]):
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
def assign_task(args: List[str]):
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
def view_tasks(_: List[str]):
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
def comment_on_task(args: List[str]):
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
def update_task_status(args: List[str]):
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
def review_task(args: List[str]):
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

@require_role(Role.MANAGER)
def create_hr_request(args: List[str]):
    global next_hr_id
    if not args:
        print("Usage: create-hr-request <type>")
        return

    req_type = " ".join(args)
    req = HRRequest(next_hr_id, req_type)
    HR_REQUESTS[next_hr_id] = req
    print(f"🧾 Created HR Request #{next_hr_id} ({req_type}) [Status: {req.status.value}]")
    next_hr_id += 1

@require_role(Role.HR_MANAGER)
def review_hr_request(args: List[str]):
    if len(args) < 2:
        print("Usage: review-hr-request <request-id> <approve|reject>")
        return

    try:
        req_id = int(args[0])
        decision = args[1].lower()
        req = HR_REQUESTS.get(req_id)
        if not req:
            print(f"❌ No HR Request with ID #{req_id}.")
            return

        match decision:
            case "approve": req.approve()
            case "reject": req.reject()
            case _: 
                print("❌ Invalid decision. Use: approve or reject.")
                return

        print(f"✅ HR Request #{req_id} updated to {req.status.value}")

    except Exception as e:
        print(f"❌ {e}")

@require_role(Role.HR_WORKER)
def hire_staff(args: List[str]):
    if len(args) < 5:
        print("Usage: hire-staff <request-id> <email> <name> <department> <duty>")
        return

    try:
        req_id = int(args[0])
        email = args[1]
        name = args[2]
        department_str = args[3].upper()
        duty = args[4]

        try:
            department = Department[department_str]
        except KeyError:
            print("❌ Invalid department. Use: PRODUCTION or SERVICES.")
            return

        req = HR_REQUESTS.get(req_id)
        if not req:
            print(f"❌ No HR Request with ID #{req_id}.")
            return

        staff = Worker(name, department, duty)

        req.hire_staff(staff)
        USERS[email] = staff

        print(f"👤 Hired {staff.name} required by HR Request #{req_id}. Status: {req.status.value}")

    except Exception as e:
        print(f"❌ {e}")

@require_role(Role.HR_MANAGER, Role.HR_WORKER)
def view_hr_requests(_: List[str]):
    if not HR_REQUESTS:
        print("No HR Requests available.")
        return
    for req in HR_REQUESTS.values():
        print(f"#{req.request_id} | {req.type} | {req.status.value} | Staff: {[w.name for w in req.hired_staff]}")

@require_role(Role.MANAGER)
def create_budget_request(args: List[str]):
    global next_budget_id
    if len(args) < 3:
        print("Usage: create-budget-request <event-id> <amount> <reason>")
        return
    try:
        event_id = int(args[0])
        amount = float(args[1])
        reason = " ".join(args[2:])
    except ValueError:
        print("❌ Invalid number format.")
        return

    req = BudgetRequest(next_budget_id, event_id, amount, reason)
    BUDGET_REQUESTS[next_budget_id] = req
    print(f"💵 Created Budget Request #{next_budget_id} for Event #{event_id} ({amount} SEK)")
    next_budget_id += 1

@require_role(Role.FIN_MANAGER)
def review_budget_request(args: List[str]):
    if len(args) < 2:
        print("Usage: review-budget-request <id> <approve|reject>")
        return
    try:
        req_id = int(args[0])
        decision = args[1].lower()
        req = BUDGET_REQUESTS.get(req_id)
        if not req:
            print(f"❌ No Budget Request #{req_id}.")
            return

        if decision == "approve":
            req.approve()
        elif decision == "reject":
            req.reject()
        else:
            print("❌ Invalid decision. Use: approve or reject.")
            return

        print(f"✅ Budget Request #{req_id} updated to {req.status.value}")
    except Exception as e:
        print(f"❌ {e}")

@require_role(Role.FIN_MANAGER)
def negotiate_budget(args: List[str]):
    global next_negotiation_id
    if len(args) < 2:
        print("Usage: negotiate-budget <request-id> <new-amount>")
        return
    try:
        req_id = int(args[0])
        new_amount = float(args[1])
        req = BUDGET_REQUESTS.get(req_id)
        if not req:
            print(f"❌ No Budget Request #{req_id}.")
            return

        negotiation = BudgetNegotiation(next_negotiation_id, req)
        negotiation.counter_offer(new_amount)
        BUDGET_NEGOTIATIONS[next_negotiation_id] = negotiation
        print(f"💬 Negotiation #{next_negotiation_id}: Counter-offer set to {new_amount} SEK.")
        next_negotiation_id += 1
    except Exception as e:
        print(f"❌ {e}")

@require_role(Role.FIN_MANAGER, Role.MANAGER)
def view_budget_requests(_: List[str]):
    if not BUDGET_REQUESTS:
        print("No budget requests available.")
        return
    for req in BUDGET_REQUESTS.values():
        print(f"#{req.request_id} | Event #{req.event_id} | {req.amount} SEK | {req.status.value} | {req.reason}")

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

                    if isinstance(CURRENT_USER, (Manager, Worker)):
                        print(f"✅ Logged in as {CURRENT_USER.name} ({CURRENT_USER.department.value} {CURRENT_USER.__class__.__name__})\n")
                    else:
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
            case "create-hr-request": create_hr_request(args)
            case "review-hr-request": review_hr_request(args)
            case "hire-staff": hire_staff(args)
            case "view-hr-requests": view_hr_requests(args)
            case "create-budget-request": create_budget_request(args)
            case "review-budget-request": review_budget_request(args)
            case "negotiate-budget": negotiate_budget(args)
            case "view-budget-requests": view_budget_requests(args)

            case _:
                print("❓ Unknown command. Type 'help' for options.")
                continue
                

def main():
    cli()

if __name__ == "__main__":
    main()