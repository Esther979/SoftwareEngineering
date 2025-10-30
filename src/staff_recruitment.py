from enum import Enum
from typing import List

from .task_distribution import Worker

class HRRequestStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    HIRED = "Hired"

class HRRequest:
    def __init__(self, request_id: int, req_type: str):
        self.request_id = request_id
        self.type = req_type
        self.status = HRRequestStatus.PENDING
        self.hired_staff: List[Worker] = []

    def approve(self):
        if self.status != HRRequestStatus.PENDING:
            raise ValueError("Only Pending requests can be approved")
        self.status = HRRequestStatus.APPROVED

    def reject(self):
        if self.status != HRRequestStatus.PENDING:
            raise ValueError("Only Pending requests can be rejected")
        self.status = HRRequestStatus.REJECTED

    def hire_staff(self, staff: Worker):
        if self.status != HRRequestStatus.APPROVED:
            raise ValueError("Request must be approved before staff hiring")
        self.hired_staff.append(staff)
        self.status = HRRequestStatus.HIRED