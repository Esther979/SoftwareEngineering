import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from budget.budget_request import BudgetRequest
from budget.negotiation import BudgetNegotiation

class TestBudgetNegotiationFlow(unittest.TestCase):

    def test_budget_negotiation_flow(self):
        print("\n===== TEST CASE: Budget Negotiation Approval Flow =====", flush=True)

        req = BudgetRequest("B01", "E01", 5000, "Decoration")
        print(f"Step 1 ✅ Created BudgetRequest -> ID: {req.request_id}, Status: {req.status}, Amount: {req.amount}", flush=True)

        neg = BudgetNegotiation("N01", req)
        print(f"Step 2 ✅ Negotiation Created -> ID: {neg.negotiation_id}, Status: {neg.status}", flush=True)

        neg.approve()
        print(f"Step 3 ✅ Negotiation Approved -> Negotiation Status: {neg.status}, Request Status: {req.status}", flush=True)

        self.assertEqual(req.status, "Approved")
        print("✅ Test Passed: Negotiation approval successfully approved the request\n", flush=True)

    def test_counter_offer(self):
        print("\n===== TEST CASE: Budget Counter Offer Updates Amount =====", flush=True)

        req = BudgetRequest("B02", "E01", 8000, "Food")
        neg = BudgetNegotiation("N02", req)
        print(f"Step 1 ✅ Initial Budget -> {req.amount}", flush=True)

        neg.counter_offer(9000)
        print(f"Step 2 ✅ Counter Offer -> New Amount: {req.amount}, Negotiation Status: {neg.status}", flush=True)

        self.assertEqual(req.amount, 9000)
        self.assertEqual(neg.status, "CounterOffer")
        print("✅ Test Passed: Counter Offer updates request amount\n", flush=True)

    def test_invalid_state_transition(self):
        print("\n===== TEST CASE: Invalid Negotiation State Transition =====", flush=True)

        req = BudgetRequest("B03", "E02", 3000, "Music")
        neg = BudgetNegotiation("N03", req)
        print("Step 1 ✅ Negotiation Created (Pending)", flush=True)

        neg.reject()
        print("Step 2 ✅ Negotiation Rejected", flush=True)

        with self.assertRaisesRegex(ValueError, "approve a rejected negotiation"):
            neg.approve()
        print("✅ Test Passed: System prevented invalid state transition\n", flush=True)


if __name__ == '__main__':
    unittest.main()
