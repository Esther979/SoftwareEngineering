import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from budget.budget_request import BudgetRequest
from budget.negotiation import BudgetNegotiation

class TestBudget(unittest.TestCase):

    def test_budget_negotiation_flow(self):
        print("\n===== Budget Negotiation Flow Test Start =====")

        req = BudgetRequest("B01", "E01", 5000, "Decoration")
        print(f"Step 1: Created BudgetRequest -> ID: {req.request_id}, Status: {req.status}")
        self.assertEqual(req.status, "Pending")

        negotiation = BudgetNegotiation("N01", req)
        print(f"Step 2: Negotiation Created -> ID: {negotiation.negotiation_id}, Status: {negotiation.status}")

        negotiation.approve()
        print(f"Step 3: Negotiation Approved -> Negotiation Status: {negotiation.status}, "
              f"Request Status: {req.status}")
        self.assertEqual(req.status, "Approved")

        print("===== Budget Negotiation Flow Test End =====\n")


if __name__ == '__main__':
    unittest.main()
