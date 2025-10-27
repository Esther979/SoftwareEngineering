import unittest
import sys
import os
sys.path.append(os.path.abspath("../")) 

from workflow.event_workflow import WorkflowSystem, EventApplication

class TestEventWorkflowWithPrint(unittest.TestCase):

    def setUp(self):
        self.system = WorkflowSystem()

    def test_workflow_and_print(self):
        app = self.system.create_event_application(
            client_name="TechCorp",
            event_type="Workshop",
            start_date="2025-12-01",
            end_date="2025-12-02",
            budget=5000,
            preferences="Audio, Decor",
            created_by="CS"
        )
        print(f"\n[CREATE] ID: {app.app_id}, Client: {app.client_name}, Status: {app.status}, Comment: {app.comment}")

        # SCS forwards
        self.system.review_application(app.app_id, "SCS", "Forwarded", "Sent to FM")
        print(f"[SCS] Status: {app.status}, Comment: {app.comment}")

        # FM feedback
        self.system.review_application(app.app_id, "FM", "Forwarded", "Budget OK")
        print(f"[FM] Status: {app.status}, Comment: {app.comment}")

        # AM approves
        self.system.review_application(app.app_id, "AM", "Approved", "")
        print(f"[AM] Status: {app.status}, Comment: {app.comment}")


        print("\n[HISTORY]")
        for record in app.history:
            print(f"Time: {record[0]}, Role: {record[1]}, Status: {record[2]}, Comment: {record[3]}")

        # ------------------- Test invalid status -------------------
        print("\n[TEST INVALID STATUS]")
        app2 = self.system.create_event_application("XCorp", "Seminar", "2025-11-01", "2025-11-03", 3000, "None")
        try:
            app2.update_status("SCS", "UNKNOWN", "Invalid status test")
        except ValueError as e:
            print(f"Caught ValueError as expected: {e}")

        # ------------------- Test get by ID -------------------
        print("\n[TEST GET APPLICATION BY ID]")
        app3 = self.system.create_event_application("Client1", "TypeA", "2025-11-01", "2025-11-02", 2000, "Decor")
        app4 = self.system.create_event_application("Client2", "TypeB", "2025-11-03", "2025-11-04", 4000, "Food")
        found = self.system.get_application_by_id(app4.app_id)
        print(f"Found by ID {app4.app_id}: Client: {found.client_name}, Status: {found.status}")

        try:
            self.system.get_application_by_id(999)
        except ValueError as e:
            print(f"Caught ValueError for non-existent ID as expected: {e}")

if __name__ == "__main__":
    unittest.main()
