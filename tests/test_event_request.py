import unittest
from datetime import datetime
from src import Role, EventSystem, EventApplicationStatus

class TestEventRequestWorkflow(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a fresh `EventSystem` for each test."""
        self.system = EventSystem()
    
    def test_create_event_application(self) -> None:
        """Verify that an event application is created with the expected initial values."""
        event_application = self.system.create_event_application(
            client_name="TestCorp",
            event_type="Workshop",
            start_date=datetime.fromisoformat("2025-12-01"),
            end_date=datetime.fromisoformat("2025-12-02"),
            budget=5000,
            preferences="Jazz music and modern decoration"
        )

        self.assertEqual(event_application.app_id, 1)
        self.assertEqual(event_application.status, EventApplicationStatus.PENDING_REVIEW)
        self.assertEqual(event_application.history[0][1], Role.CS_WORKER)

        self.assertEqual(event_application.client_name, "TestCorp")
        self.assertEqual(event_application.event_type, "Workshop")
        self.assertEqual(event_application.start_date, datetime.fromisoformat("2025-12-01"))
        self.assertEqual(event_application.end_date, datetime.fromisoformat("2025-12-02"))
        self.assertEqual(event_application.budget, 5000)
        self.assertEqual(event_application.preferences, "Jazz music and modern decoration")

    def test_review_application_forward_by_senior_customer_service_officer(self):
        """Test that Senior Customer Service Officer can forward an application successfully."""
        event_application = self.system.create_event_application(
            client_name="TestCorp",
            event_type="Workshop",
            start_date=datetime.fromisoformat("2025-12-01"),
            end_date=datetime.fromisoformat("2025-12-02"),
            budget=5000,
            preferences="Jazz music and modern decoration"
        )

        updated = self.system.review_application(
            app_id=event_application.app_id,
            role=Role.CS_MANAGER,
            decision=EventApplicationStatus.FORWARDED,
            comment="Forwarding to financial manager"
        )

        self.assertEqual(updated.status, EventApplicationStatus.FORWARDED)
        self.assertIn((Role.CS_MANAGER), [h[1] for h in updated.history])
        self.assertEqual(updated.history[-1][2], EventApplicationStatus.FORWARDED.value)

    def test_financial_manager_can_only_act_after_forwarded(self):
        """Test that the Financial Manager cannot act before the CS Worker forwards the application."""
        event_application = self.system.create_event_application(
            client_name="TestCorp",
            event_type="Workshop",
            start_date=datetime.fromisoformat("2025-12-01"),
            end_date=datetime.fromisoformat("2025-12-02"),
            budget=5000,
            preferences="Jazz music and modern decoration"
        )

        with self.assertRaises(ValueError) as cm:
            self.system.review_application(
                app_id=event_application.app_id,
                role=Role.FIN_MANAGER,
                decision=EventApplicationStatus.APPROVED,
                comment="Looks good"
            )
        self.assertIn("FM can only act after SCS has forwarded", str(cm.exception))

    def test_financial_manager_can_review_after_forwarded(self):
        """Test that Financial Manager can approve after Customer Service forwards."""
        event_application = self.system.create_event_application(
            client_name="TestCorp",
            event_type="Workshop",
            start_date=datetime.fromisoformat("2025-12-01"),
            end_date=datetime.fromisoformat("2025-12-02"),
            budget=5000,
            preferences="Jazz music and modern decoration"
        )

        # Step 1: Senior Customer Service Officer forwards
        self.system.review_application(event_application.app_id, Role.CS_MANAGER, EventApplicationStatus.FORWARDED, "Ready for FM review")

        # Step 2: Financial Manager approves
        updated = self.system.review_application(event_application.app_id, Role.FIN_MANAGER, EventApplicationStatus.APPROVED, "Budget OK")

        self.assertEqual(updated.status, EventApplicationStatus.APPROVED)
        self.assertEqual(updated.comment, "Budget OK")
        self.assertIn(Role.FIN_MANAGER, [h[1] for h in updated.history])

    def test_administration_manager_cannot_act_before_financial_manager(self):
        """Test that Administration Manager cannot act before Financial Manager has reviewed."""
        event_application = self.system.create_event_application(
            client_name="TestCorp",
            event_type="Workshop",
            start_date=datetime.fromisoformat("2025-12-01"),
            end_date=datetime.fromisoformat("2025-12-02"),
            budget=5000,
            preferences="Jazz music and modern decoration"
        )

        # Forwarded by Senior Customer Service Officer.
        self.system.review_application(event_application.app_id, Role.CS_MANAGER, EventApplicationStatus.FORWARDED, "Forward to FM")

        # Administration Manager tries to approve before Financial Manager acts
        with self.assertRaises(ValueError) as cm:
            self.system.review_application(event_application.app_id, Role.ADM_MANAGER, EventApplicationStatus.APPROVED, "All good")
        self.assertIn("AM cannot act before FM has reviewed", str(cm.exception))
