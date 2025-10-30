from app.service import UserService
from app.auth import Role
from hr.hr_request import HRRequest
from hr.staff_member import StaffMember
from budget.budget_request import BudgetRequest
from budget.negotiation import BudgetNegotiation


class CLI:

    def __init__(self):
        self.user = None
        self.hr_requests = {}
        self.budget_requests = {}
        self.negotiations = {}

    def login(self):
        print("====== Welcome to SEP Internal System ======")
        print("1. HR")
        print("2. Financial Manager")
        print("3. Production Manager")
        choice = input("Select your role: ")

        if choice == "1":
            self.user = UserService(Role.HR)
        elif choice == "2":
            self.user = UserService(Role.FM)
        elif choice == "3":
            self.user = UserService(Role.PM)
        else:
            print("Invalid selection!")
            return self.login()

        print(f"✅ Logged in as: {self.user.role}\n")
        self.show_menu()

    # ================= Menus ================= #

    def show_menu(self):
        if self.user.role == Role.HR:
            self.show_hr_menu()
        elif self.user.role == Role.FM:
            self.show_fm_menu()
        elif self.user.role == Role.PM:
            self.show_pm_menu()

    def show_hr_menu(self):
        print("--- HR Menu ---")
        print("1) Approve HR Request")
        print("2) Assign Staff")
        print("3) Reject HR Request")
        print("0) Logout")
        self.handle_hr_action()

    def show_fm_menu(self):
        print("--- Financial Manager Menu ---")
        print("1) Approve Budget")
        print("2) Reject Budget")
        print("3) Counter Offer")
        print("0) Logout")
        self.handle_fm_action()

    def show_pm_menu(self):
        print("--- Production Manager Menu ---")
        print("1) Create HR Request")
        print("2) Create Budget Request")
        print("0) Logout")
        self.handle_pm_action()

    # ================= HR Actions ================= #

    def handle_hr_action(self):
        action = input("Select action: ")

        if action == "1":
            req_id = input("Enter HR request ID: ")
            req = self.hr_requests.get(req_id)
            if req:
                self.user.approve_hr_request(req)
                print("✅ Approved!")
            else:
                print("❌ Not Found")

        elif action == "2":
            req_id = input("Enter HR request ID: ")
            req = self.hr_requests.get(req_id)
            if req:
                name = input("Assign Staff Name: ")
                staff = StaffMember(name, "X100", "Chef", "Services")
                self.user.assign_staff(req, staff)
                print("✅ Staff Assigned!")
            else:
                print("❌ Request Not Found")

        elif action == "3":
            req_id = input("Enter HR request ID: ")
            req = self.hr_requests.get(req_id)
            if req:
                self.user.reject_hr_request(req)
                print("❌ Rejected")
            else:
                print("Not Found")

        elif action == "0":
            self.login()
        else:
            print("Invalid")
        self.show_hr_menu()

    # ================= FM Actions ================= #
    def handle_fm_action(self):
        action = input("Select action: ")

        if action == "1":
            nid = input("Negotiation ID: ")
            neg = self.negotiations.get(nid)
            if neg:
                self.user.approve_budget(neg)
                print("✅ Approved")
            else:
                print("❌ Not Found")

        elif action == "2":
            nid = input("Negotiation ID: ")
            neg = self.negotiations.get(nid)
            if neg:
                self.user.reject_budget(neg)
                print("❌ Rejected")
            else:
                print("Not Found")

        elif action == "3":
            nid = input("Negotiation ID: ")
            neg = self.negotiations.get(nid)
            if neg:
                amount = int(input("New Amount: "))
                self.user.counter_offer(neg, amount)
                print("🔁 Counter Offer Sent")
            else:
                print("Not Found")

        elif action == "0":
            self.login()

        self.show_fm_menu()

    # ================= PM Actions ================= #
    def handle_pm_action(self):
        action = input("Select action: ")

        if action == "1":
            req_id = input("New HR Request ID: ")
            req = self.user.create_hr_request(req_id, "Recruitment")
            self.hr_requests[req_id] = req
            print("✅ Created HR Request")

        elif action == "2":
            req_id = input("New Budget Request ID: ")
            event_id = input("Event ID: ")
            amount = int(input("Amount: "))
            reason = input("Reason: ")
            req = self.user.create_budget_request(req_id, event_id, amount, reason)
            self.budget_requests[req_id] = req
            neg = BudgetNegotiation("N"+req_id, req)
            self.negotiations["N"+req_id] = neg
            print("✅ Created Budget Request + Negotiation")

        elif action == "0":
            self.login()

        self.show_pm_menu()

if __name__ == "__main__":
    CLI().login()
