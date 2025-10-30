# SEP - Swedish Events Planners

An interactive **Command-Line Interface (CLI)** simulation for managing internal operations at SEP — including event applications, task distribution, HR recruitment, and financial requests.

The system models multiple roles such as **Customer Service**, **Managers**, **Workers**, **HR**, and **Finance**, all operating in a shared in-memory workflow.

---

## Features

### 🌐 Event Management
- **Customer Service Officers** create event applications.
- **Senior Customer Officer** and **Finance/Administration Manager** review and approve them.
- Full event history and status tracking.

### 🧠 Task Workflow
- **Production/Services Managers** create, assign, and update tasks.
- **Workers** comment and request budgets.
- All within the same in-memory session.

### 👥 HR Recruitment
- **HR Managers** approve requests.
- **HR Workers** hire new staff dynamically.
- Updates the in-memory employee database instantly.

### 💰 Financial Requests
- **Production/Services Managers** create budget requests.
- **Finance Managers** review or negotiate them.

---

## Getting Started

### Run the CLI

```bash
python main.py
```

> **Note:** No persistent storage: All data exists only during the current session.

### Testing

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Example CLI Session

```bash
$ python main.py 

SEP Internal System CLI ⚙️
Type 'help' to see available commands.

> help

Available commands:
  login <email>                      Log in
  help                               Show this help
  quit                               Exit the program

> login mike@sep.se
✅ Logged in as Mike (Employee, Administration Department Manager)

[Mike] > help

Available commands:
  view-event-application <app_id>
  review-event-application <app_id> <FORWARDED|APPROVED|REJECTED> <comment>
  logout                                  Log out
  quit                                    Exit program

[Mike] > view-event-application 1
❌ No application found with ID 1
[Mike] > logout
👋 Logged out

> login sarah@sep.se
✅ Logged in as Sarah (Employee, Customer Service Officer)

[Sarah] > create-event-application "TestCorp" "Workshop" "2025-12-01" "2025-12-02" 5000 "Modern theme"
🆕 Created Event Application #1 for TestCorp
[Sarah] > logout
👋 Logged out

> login janet@sep.se
✅ Logged in as Janet (Employee, Senior Customer Service Officer)

[Janet] > review-event-application 1 FORWARDED "Forwarding to financial review"
✅ Application #1 updated to Forwarded
[Janet] > logout
👋 Logged out

> quit
👋 Goodbye!
```

## Authors

**Group 7:** 
- Jingmeng Xie
- Erick Castillo
- Luyao Wang
