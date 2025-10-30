from enum import Enum

class BudgetRequestStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class BudgetNegotiationStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    COUNTER_OFFER = "Counter Offer"

class BudgetRequest:
    def __init__(self, request_id: int, event_id: int, amount: float, reason: str):
        self.request_id = request_id
        self.event_id = event_id
        self.amount = amount
        self.reason = reason
        self.status = BudgetRequestStatus.PENDING

    def approve(self):
        self.status = BudgetRequestStatus.APPROVED

    def reject(self):
        self.status = BudgetRequestStatus.REJECTED

class BudgetNegotiation:
    def __init__(self, negotiation_id: int, request: BudgetRequest):
        self.negotiation_id = negotiation_id
        self.request = request
        self.status = BudgetNegotiationStatus.PENDING

    def approve(self):
        if self.status == BudgetNegotiationStatus.REJECTED:
            raise ValueError("Cannot approve a rejected negotiation")
        self.status = BudgetNegotiationStatus.APPROVED
        self.request.approve()

    def reject(self):
        if self.status == BudgetNegotiationStatus.APPROVED:
            raise ValueError("Cannot reject an already approved negotiation")
        self.status = BudgetNegotiationStatus.REJECTED
        self.request.reject()

    def counter_offer(self, new_amount: float):
        if self.status not in [BudgetNegotiationStatus.PENDING, BudgetNegotiationStatus.COUNTER_OFFER]:
            raise ValueError("Cannot counter offer after approval/rejection")
        self.status = BudgetNegotiationStatus.COUNTER_OFFER
        self.request.amount = new_amount