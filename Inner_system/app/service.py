from app.auth import Role, require_permission
from hr.hr_request import HRRequest
from hr.staff_member import StaffMember
from budget.budget_request import BudgetRequest
from budget.negotiation import BudgetNegotiation


class UserService:
    def __init__(self, role):
        self.role = role

    # --- HR functions ---
    @require_permission("create_hr_request")
    def create_hr_request(self, request_id, req_type):
        print("Creating HR Request...")
        return HRRequest(request_id, req_type)

    @require_permission("approve_hr_request")
    def approve_hr_request(self, request: HRRequest):
        request.approve()

    @require_permission("reject_hr_request")
    def reject_hr_request(self, request: HRRequest):
        request.reject()

    @require_permission("assign_staff")
    def assign_staff(self, request: HRRequest, staff: StaffMember):
        request.assign_staff(staff)

    # --- Budget functions ---
    @require_permission("create_budget_request")
    def create_budget_request(self, req_id, event_id, amount, reason):
        return BudgetRequest(req_id, event_id, amount, reason)

    @require_permission("approve_budget")
    def approve_budget(self, negotiation: BudgetNegotiation):
        negotiation.approve()

    @require_permission("reject_budget")
    def reject_budget(self, negotiation: BudgetNegotiation):
        negotiation.reject()

    @require_permission("counter_offer")
    def counter_offer(self, negotiation: BudgetNegotiation, amount):
        negotiation.counter_offer(amount)
