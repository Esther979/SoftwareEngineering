from enum import Enum

class Role(Enum):
    ADM_MANAGER = "Administration Department Manager"
    FIN_MANAGER = "Financial Manager"
    HR_MANAGER = "Human Resources Manager"
    HR_WORKER = "Human Resources Agent"
    CS_MANAGER = "Senior Customer Service Officer"
    CS_WORKER = "Customer Service Officer"
    MANAGER = "Manager"
    WORKER = "Staff Member"

class Employee():
    def __init__(self, name: str, role: Role) -> None:
        self.name = name
        self.role = role
