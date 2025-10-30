from datetime import datetime

class EventApplication:
    def __init__(self, app_id, client_name, event_type, start_date, end_date, budget, preferences, created_by):
        self.app_id = app_id
        self.client_name = client_name
        self.event_type = event_type
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.preferences = preferences
        self.created_by = created_by
        self.status = "Pending Review"
        self.history = [(datetime.now(), created_by, "Created", "Initial submission")]
        self.comment = ""  

    def update_status(self, user_role, new_status, comment=""):
        valid_statuses = ["Pending Review", "Forwarded", "Approved", "Rejected"]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}")
        self.status = new_status
        if user_role == "FM" and comment:
            self.comment = comment  
        self.history.append((datetime.now(), user_role, new_status, comment))

    def __str__(self):
        return f"[#{self.app_id}] {self.client_name} - {self.event_type} ({self.status})"


class WorkflowSystem:
    def __init__(self):
        self.applications = []
        self.next_id = 1

    def create_event_application(self, client_name, event_type, start_date, end_date, budget, preferences, created_by="CustomerService"):
        app = EventApplication(
            app_id=self.next_id,
            client_name=client_name,
            event_type=event_type,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            preferences=preferences,
            created_by=created_by
        )
        self.applications.append(app)
        self.next_id += 1
        return app

    def review_application(self, app_id, role, decision, comment):
        app = self.get_application_by_id(app_id)

        
        if role == "FM":
            if app.status != "Forwarded":
                raise ValueError("FM can only act after SCS has forwarded the application.")
        elif role == "AM":
            last_roles = [r[1] for r in app.history]
            if "FM" not in last_roles:
                raise ValueError("AM cannot act before FM has reviewed the application.")


        if decision not in ["Forwarded", "Approved", "Rejected"]:
            raise ValueError(f"Invalid decision: {decision}")

        app.update_status(role, decision, comment)


        if role == "FM" and comment:
            app.comment = comment

        return app

    def get_application_by_id(self, app_id):
        for app in self.applications:
            if app.app_id == app_id:
                return app
        raise ValueError(f"No application found with ID {app_id}")

    def list_applications(self):
        return [str(app) for app in self.applications]
