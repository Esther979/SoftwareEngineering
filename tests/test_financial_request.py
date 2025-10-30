import unittest

from src import BudgetRequest, BudgetRequestStatus, BudgetNegotiation, BudgetNegotiationStatus

class TestFinancialRequestWorkflow(unittest.TestCase):

    def setUp(self) -> None:
        """Set up a fresh budget request for each test."""
        self.request = BudgetRequest(request_id=1, event_id=1, amount=50000.0, reason="Decoration")
        self.negotiation = BudgetNegotiation(1, self.request)

    def test_initial_status_is_pending(self) -> None:
        """Newly created budget requests should start with `Pending` status."""
        self.assertEqual(self.request.status, BudgetRequestStatus.PENDING)

    def test_can_approve_budget_request(self) -> None:
        """A budget request can be approved by a financial manager."""
        self.request.approve()
        self.assertEqual(self.request.status, BudgetRequestStatus.APPROVED)

    def test_can_reject_budget_request(self) -> None:
        """A budget request can be rejected."""
        self.request.reject()
        self.assertEqual(self.request.status, BudgetRequestStatus.REJECTED)
    
    def test_budget_negotiation_initial_status_is_pending(self) -> None:
        """Negotiations should begin in 'Pending' status."""
        self.assertEqual(self.negotiation.status, BudgetNegotiationStatus.PENDING)

    def test_counter_offer_updates_request_and_status(self) -> None:
        """Counter-offers should update both negotiation status and request amount."""
        self.negotiation.counter_offer(65000.0)
        self.assertEqual(self.negotiation.status, BudgetNegotiationStatus.COUNTER_OFFER)
        self.assertEqual(self.request.amount, 65000.0)

    def test_approve_negotiation_sets_approved_status(self) -> None:
        """Approving a negotiation should mark both negotiation and request as approved."""
        self.negotiation.approve()
        self.assertEqual(self.negotiation.status, BudgetNegotiationStatus.APPROVED)
        self.assertEqual(self.request.status, BudgetRequestStatus.APPROVED)

    def test_reject_negotiation_sets_rejected_status(self) -> None:
        """Rejecting a negotiation should mark both negotiation and request as rejected."""
        self.negotiation.reject()
        self.assertEqual(self.negotiation.status, BudgetNegotiationStatus.REJECTED)
        self.assertEqual(self.request.status, BudgetRequestStatus.REJECTED)

    def test_cannot_approve_after_rejection(self) -> None:
        """Cannot approve a negotiation after it has been rejected."""
        self.negotiation.reject()
        with self.assertRaises(ValueError):
            self.negotiation.approve()

    def test_cannot_reject_after_approval(self) -> None:
        """Cannot reject a negotiation after it has been approved."""
        self.negotiation.approve()
        with self.assertRaises(ValueError):
            self.negotiation.reject()

    def test_invalid_counter_offer_after_closure(self) -> None:
        """Cannot counter-offer after negotiation has been approved or rejected."""
        self.negotiation.approve()
        with self.assertRaises(ValueError):
            self.negotiation.counter_offer(70000.0)


if __name__ == "__main__":
    unittest.main()