# Group7_Software Project
## Workflow 1

## Workflow 2

## Workflow 3 and Workflow 4
### 1. Environment
**Python version:** Python 3.9  
**Required libraries:**
No external dependencies — only Python standard libraries are used (unittest, os, sys).  
**Path:** `cd ~/SoftwareEngineer/Inner_system/`  

### 2. Structure
```ruby
Inner_system
├── app
│   ├── cli.py
│   ├── service.py
│   ├── auth.py
│   └── __init__.py
├── hr
│   ├── hr_request.py
│   ├── staff_member.py
│   └── __init__.py
├── budget
│   ├── budget_request.py
│   ├── negotiation.py
│   └── __init__.py
├── tests
│   ├── test_hr.py
│   ├── test_hr2.py
│   ├── test_budget.py
│   ├── test_budget2.py
│   ├── test_auth.py
│   └── __init__.py
├── main.py
├── README.md
└── __init__.py
```

### 3. Test Command
**Unit Tests:** `python3 -m unittest discover -s tests -v`  
**Acceptance Tests:** `python3 -m app.cli`

### 4. Core Functionalities
- **HR Request Management**: Recruitment request approval and staff assignment workflow.  
- **Budget Request & Negotiation**: Financial negotiation and approval process with counter offers.  
- **RBAC (Role-Based Access Control)**: Enforces permissions for HR, Financial Manager (FM), and Project Manager (PM).  
- **Automated Unit Testing**: All components verified via `unittest` under the TDD cycle.  

### 5. Expected Behavior
HRRequest Workflow: `Pending → Approved → Fulfilled`  
Assigning staff before approval raises: `ValueError("HR request must be approved before staff assignment")`  
BudgetNegotiation Workflow: `Pending → CounterOffer → Approved / Rejected`  
Approving after rejection raises: `ValueError("Cannot approve a rejected negotiation")`  

Author: Jingmeng Xie  
Date: 2025.10.28  


