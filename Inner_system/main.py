from app.service import UserService
from app.auth import Role
from hr.staff_member import StaffMember
from budget.negotiation import BudgetNegotiation

# PM creates request
pm = UserService(Role.PM)
hr_request = pm.create_hr_request("HR05", "Recruitment")

# HR handles request
hr = UserService(Role.HR)
hr.approve_hr_request(hr_request)
hr.assign_staff(hr_request, StaffMember("Tom", "S200", "Chef", "Services"))

# FM handles budget request
fm = UserService(Role.FM)
budget_request = pm.create_budget_request("B99", "E99", 10000, "Lighting")
neg = BudgetNegotiation("N99", budget_request)
fm.counter_offer(neg, 12000)
fm.approve_budget(neg)
