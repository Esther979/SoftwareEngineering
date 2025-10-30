import unittest

from src import HRRequest, HRRequestStatus, Department, Worker

class TestStaffRecruitmentWorkflow(unittest.TestCase):
    def setUp(self) -> None:
        """Prepare a fresh HR request for each test."""
        self.request = HRRequest(1, "Hire Production Staff")

    def test_initial_status_is_pending(self) -> None:
        """HR request starts in 'Pending' state."""
        self.assertEqual(self.request.status, HRRequestStatus.PENDING)
        self.assertEqual(len(self.request.hired_staff), 0)

    def test_approve_changes_status_to_approved(self) -> None:
        """Approving a pending HR request should change its status to 'Approved'."""
        self.request.approve()
        self.assertEqual(self.request.status, HRRequestStatus.APPROVED)

    def test_reject_changes_status_to_rejected(self) -> None:
        """Rejecting a pending HR request should change its status to 'Rejected'."""
        self.request.reject()
        self.assertEqual(self.request.status, HRRequestStatus.REJECTED)

    def test_cannot_approve_non_pending_request(self) -> None:
        """Once rejected or hired, an HR request cannot be approved again."""
        self.request.reject()
        with self.assertRaises(ValueError):
            self.request.approve()

    def test_cannot_reject_non_pending_request(self) -> None:
        """Once approved or hired, an HR request cannot be rejected again."""
        self.request.approve()
        with self.assertRaises(ValueError):
            self.request.reject()

    def test_can_hire_staff_after_approval(self) -> None:
        """Approved HR requests allow hiring workers."""
        self.request.approve()
        worker = Worker("John", Department.PRODUCTION, "Technician")
        self.request.hire_staff(worker)

        self.assertIn(worker, self.request.hired_staff)
        self.assertEqual(self.request.status, HRRequestStatus.HIRED)

    def test_cannot_hire_staff_before_approval(self) -> None:
        """Hiring before approval should raise an error."""
        worker = Worker("John", Department.PRODUCTION, "Technician")
        with self.assertRaises(ValueError):
            self.request.hire_staff(worker)

if __name__ == "__main__":
    unittest.main()