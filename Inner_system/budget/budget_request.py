class BudgetRequest:
    def __init__(self, request_id, event_id, amount, reason):
        self.request_id = request_id
        self.event_id = event_id
        self.amount = amount
        self.reason = reason
        self.status = "Pending"

    def approve(self):
        self.status = "Approved"

    def reject(self):
        self.status = "Rejected"
