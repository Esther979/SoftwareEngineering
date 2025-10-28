# Group7_Software Project
## Workflow 1
### 1. Environment
Python version: Python 3.11.4   
Path: `cd ~/SoftwareEngineering/event_workflow/`

### 2.Structure    
event_workflow/     
├── app/    
│   └── event_workflow_gui.py   
│   └── __init__.py     
├── workflow/   
│   └── event_workflow.py   
│   └── __init__.py     
├── tests/  
│   ├── gui_test.py     
│   └── test_event_workflow.py      
│   └── __init__.py  
├── main.py     
└── README.md   

### 3.Test Command    
Unit Tests :    
`python -m unittest discover -s tests -p "*.py" -v`    
`python -m unittest discover -s tests -p "gui_test.py" -v`  

Acceptance Tests :  
`python -m app.event_workflow_gui`

### 4.Core Functionalities  
1. Create event application     
    **Customer Service**: Create an event application by entering details of event. 

2. Application Review   
    **Senior Customer Service**: Review the application and decides whether to reject or forward it.    

    **Financial Manager**: Write feedbacks on the budget and redirect it to the administration manager.     

    **Administration manager**: Approve or reject the application based on the feedbacks of financial manager.  

### 5.Expected Behavior 
Event Application Workflow: `CustomerService → SeniorCustomerService → FinancialManager → AdministrationManager`    
   1. Creating a new application automatically sets: `status = "Pending Review"`    
   2. When each role acts, the workflow progresses through:
`Pending Review → Forwarded/Rejected → Approved / Rejected` 

Error Handling:     
   1. If FM tries to review before SCS has forwarded:
`ValueError("FM can only act after SCS has forwarded the application.")`
   2. If AM tries to approve before FM review:
`ValueError("AM cannot act before FM has reviewed the application.")`
   3. If an invalid status is used:
`ValueError("Invalid status: <STATUS>")`

## Workflow 2

## Workflow 3 and Workflow 4
### 1. Environment
**Python version:** Python 3.9  
**Required libraries:**
No external dependencies — only Python standard libraries are used (unittest, os, sys).  
**Path:** `cd ~/SoftwareEngineering/Inner_system/`  

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




