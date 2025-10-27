import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from hr.hr_request import HRRequest
from hr.staff_member import StaffMember

class TestHRStatusFlow(unittest.TestCase):

    def test_hr_assign_staff_fulfills_request(self):
        print("\n===== TEST CASE: Assign Staff After Approval =====", flush=True)

        req = HRRequest("HR02", "Recruitment")
        print(f"Step 1 ✅ Created HRRequest -> ID: {req.request_id}, Status: {req.status}", flush=True)

        req.approve()
        print(f"Step 2 ✅ Approved Request -> Status: {req.status}", flush=True)

        staff = StaffMember("Bob", "S101", "Waiter", "Services")
        print(f"Step 3 ✅ Staff Prepared -> Name: {staff.name}, Status: {staff.status}", flush=True)

        req.assign_staff(staff)
        print(f"Step 4 ✅ Staff Assigned -> HRRequest Status: {req.status}, Staff Status: {staff.status}", flush=True)

        self.assertEqual(req.status, "Fulfilled")
        print("✅ Test Passed: HR Request fulfilled after staff assignment\n", flush=True)

    def test_invalid_staff_assign_before_approve(self):
        print("\n===== TEST CASE: Assign Staff While Pending =====", flush=True)

        req = HRRequest("HR03", "Recruitment")
        staff = StaffMember("Leo", "S102", "Chef", "Services")
        print(f"Created HRRequest (Pending) and Staff: {staff.name}", flush=True)

        with self.assertRaisesRegex(ValueError, "approved before staff assignment"):
            req.assign_staff(staff)
        print("✅ Test Passed: System blocked invalid action and threw ValueError\n", flush=True)


if __name__ == '__main__':
    unittest.main()
