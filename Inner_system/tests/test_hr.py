import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from hr.hr_request import HRRequest
from hr.staff_member import StaffMember

class TestHR(unittest.TestCase):

    def test_hr_request_flow(self):
        print("\n===== HR Request Flow Test Start =====")

        req = HRRequest("HR01", "Recruitment")
        print(f"Step 1: Created HRRequest -> ID: {req.request_id}, Status: {req.status}")

        req.approve()
        print(f"Step 2: Request Approved -> Status: {req.status}")
        self.assertEqual(req.status, "Approved")

        new_staff = StaffMember("Lisa", "S100", "Chef", "Services")
        print(f"Step 3: New Staff Created -> Name: {new_staff.name}, Status: {new_staff.status}")

        req.assign_staff(new_staff)
        print(f"Step 4: Staff Assigned -> {new_staff.name} Status: {new_staff.status}")
        self.assertEqual(new_staff.status, "Hired")

        print("===== HR Request Flow Test End =====\n")


if __name__ == '__main__':
    unittest.main()
