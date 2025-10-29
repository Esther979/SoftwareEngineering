from enum import Enum
from datetime import datetime
from typing import List, Tuple

from .models import Role

class EventApplicationStatus(Enum):
    PENDING_REVIEW = "Pending Review"
    FORWARDED = "Forwarded"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class EventApplication:
    def __init__(self, app_id: int, client_name: str, event_type: str, 
                 start_date: datetime, end_date: datetime, budget: float, 
                 preferences: str, created_by: Role) -> None:
        self.app_id: int = app_id
        self.client_name: str = client_name
        self.event_type: str = event_type
        self.start_date: datetime = start_date
        self.end_date: datetime = end_date
        self.budget: float = budget
        self.preferences: str = preferences
        self.created_by: Role = created_by
        self.status: EventApplicationStatus = EventApplicationStatus.PENDING_REVIEW
        self.history: List[Tuple[datetime, Role, str, str]] = [(datetime.now(), created_by, "Created", "Initial submission")]
        self.comment: str = ""  

    def update_status(self, user_role: Role, new_status: EventApplicationStatus, comment: str = "") -> None:
        if new_status not in EventApplicationStatus.__members__:
            raise ValueError(f"Invalid status: {new_status}")
        self.status = new_status

        if user_role == Role.FIN_MANAGER and comment:
            self.comment = comment  
        self.history.append((datetime.now(), user_role, new_status.value, comment))

    def __str__(self) -> str:
        return f"[#{self.app_id}] {self.client_name} - {self.event_type} ({self.status})"


class WorkflowSystem:
    def __init__(self) -> None:
        self.applications: List[EventApplication] = []
        self.next_id: int = 1

    def create_event_application(self, client_name: str, event_type: str, 
                               start_date: datetime, end_date: datetime, 
                               budget: float, preferences: str, 
                               created_by: Role = Role.CS_WORKER) -> EventApplication:
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

    def review_application(self, app_id: int, role: Role, 
                         decision: EventApplicationStatus, comment: str) -> EventApplication:
        app = self.get_application_by_id(app_id)

        if role is Role.FIN_MANAGER:
            if app.status is not EventApplicationStatus.FORWARDED:
                raise ValueError("FM can only act after SCS has forwarded the application.")
        elif role is Role.ADM_MANAGER:
            last_roles = [r[1] for r in app.history]
            if Role.FIN_MANAGER not in last_roles:
                raise ValueError("AM cannot act before FM has reviewed the application.")

        if decision not in [EventApplicationStatus.FORWARDED, EventApplicationStatus.APPROVED, EventApplicationStatus.REJECTED]:
            raise ValueError(f"Invalid decision: {decision}")

        app.update_status(role, decision, comment)

        if role is Role.FIN_MANAGER and comment:
            app.comment = comment

        return app

    def get_application_by_id(self, app_id: int) -> EventApplication:
        for app in self.applications:
            if app.app_id == app_id:
                return app
        raise ValueError(f"No application found with ID {app_id}")

    def list_applications(self) -> List[str]:
        return [str(app) for app in self.applications]