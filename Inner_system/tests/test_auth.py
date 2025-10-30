import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from app.service import UserService
from app.auth import Role
from hr.hr_request import HRRequest
from hr.staff_member import StaffMember
from budget.budget_request import BudgetRequest
from budget.negotiation import BudgetNegotiation


class TestPermissions(unittest.TestCase):

    def test_hr_can_approve_hr_request(self):
        print("\n===== TEST CASE: HR Approves HR Request =====", flush=True)

        hr = UserService(Role.HR)
        req = HRRequest("HR10", "Recruitment")
        
        hr.approve_hr_request(req)
        self.assertEqual(req.status, "Approved")
        print("✅ HR was allowed to approve HR request\n", flush=True)


    def test_pm_cannot_approve_hr_request(self):
        print("\n===== TEST CASE: PM Cannot Approve HR Request =====", flush=True)

        pm = UserService(Role.PM)
        req = HRRequest("HR11", "Recruitment")

        with self.assertRaises(PermissionError):
            pm.approve_hr_request(req)
        print("✅ PermissionError correctly triggered\n", flush=True)


    def test_fm_can_manage_budget(self):
        print("\n===== TEST CASE: FM Manages Budget Request =====", flush=True)

        fm = UserService(Role.FM)
        req = BudgetRequest("B10", "E10", 7000, "Audio")
        neg = BudgetNegotiation("N10", req)

        fm.counter_offer(neg, 7500)
        fm.approve_budget(neg)

        self.assertEqual(req.status, "Approved")
        print("✅ FM successfully processed budget\n", flush=True)


    def test_hr_cannot_manage_budget(self):
        print("\n===== TEST CASE: HR Cannot Manage Budget =====", flush=True)

        hr = UserService(Role.HR)
        req = BudgetRequest("B11", "E11", 9000, "Food")
        neg = BudgetNegotiation("N11", req)

        with self.assertRaises(PermissionError):
            hr.approve_budget(neg)
        print("✅ PermissionError correctly triggered\n", flush=True)


if __name__ == "__main__":
    unittest.main()
