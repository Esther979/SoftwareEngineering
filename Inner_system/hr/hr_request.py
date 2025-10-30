class HRRequest:
    def __init__(self, request_id, req_type):
        self.request_id = request_id
        self.type = req_type
        self.status = "Pending"
        self.assigned_staff = []

    def approve(self):
        if self.status != "Pending":
            raise ValueError("Only Pending requests can be approved")
        self.status = "Approved"

    def reject(self):
        if self.status != "Pending":
            raise ValueError("Only Pending requests can be rejected")
        self.status = "Rejected"

    def assign_staff(self, staff):
        if self.status != "Approved":
            raise ValueError("Request must be approved before staff assignment")
        staff.status = "Hired"
        self.assigned_staff.append(staff)
        # if at least one is assigned → Request completed
        self.status = "Fulfilled"
