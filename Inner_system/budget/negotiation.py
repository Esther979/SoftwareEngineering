class BudgetNegotiation:
    def __init__(self, negotiation_id, request):
        self.negotiation_id = negotiation_id
        self.request = request
        self.status = "Pending"

    def approve(self):
        if self.status == "Rejected":
            raise ValueError("Cannot approve a rejected negotiation")
        self.status = "Approved"
        self.request.approve()

    def reject(self):
        if self.status == "Approved":
            raise ValueError("Cannot reject an already approved negotiation")
        self.status = "Rejected"
        self.request.reject()

    def counter_offer(self, new_amount):
        if self.status not in ["Pending", "CounterOffer"]:
            raise ValueError("Cannot counter offer after approval/rejection")
        self.status = "CounterOffer"
        self.request.amount = new_amount
