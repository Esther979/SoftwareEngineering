from enum import Enum
from datetime import datetime
from typing import List, TypedDict

from .models import Employee, Role

class Department(Enum):
    PRODUCTION = "Production"
    SERVICES = "Services"

class TaskStatus(Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    CLOSED = "Closed"

class Comment(TypedDict):
    worker: str
    comment: str
    timestamp: datetime

class BudgetRequest(TypedDict):
    worker: str
    amount: float
    reason: str
    timestamp: datetime

class Task():
    def __init__(self, event_id: int, title: str, description: str, department: Department) -> None:
        self.event_id: int = event_id
        self.title: str = title
        self.description: str = description
        self.department: Department = department
        self.assigned_workers: List[Worker] = []
        self.status: TaskStatus = TaskStatus.OPEN
        self.comments: List[Comment] = []
        self.budget_requests: List[BudgetRequest] = []
        self.created_at: datetime = datetime.now()

    def add_comment(self, worker_name: str, comment: str) -> None:
        self.comments.append({
            "worker": worker_name, 
            "comment": comment, 
            "timestamp": datetime.now()
        })

    def add_budget_request(self, worker_name: str, amount: float, reason: str) -> None:
        self.budget_requests.append({
            "worker": worker_name,
            "amount": amount,
            "reason": reason,
            "timestamp": datetime.now()
        })

    def __repr__(self) -> str:
        return f"<Task [EID: {self.event_id}] '{self.title}' ({self.status.value})>"

class Worker(Employee):
    def __init__(self, name: str, department: Department, duty: str) -> None:
        super().__init__(name, Role.WORKER)
        self.department: Department = department
        self.duty: str = duty 
        self.tasks: List[Task] = []

    def view_tasks(self) -> List[Task]:
        return self.tasks

    def comment_on_task(self, task: Task, comment: str) -> None:
        if task not in self.tasks:
            raise PermissionError("You are not assigned to this task.")

        task.add_comment(self.name, comment)

    def request_more_budget(self, task: Task, amount: float, reason: str) -> None:
        if task not in self.tasks:
            raise PermissionError("You are not assigned to this task.")
        
        task.add_budget_request(self.name, amount, reason)

class Manager(Employee):
    def __init__(self, name: str, department: Department) -> None:
        super().__init__(name, Role.MANAGER)
        self.department: Department = department
        self.tasks: List[Task] = []
    
    def create_task(self, event_id: int, title: str, description: str) -> Task:
        task = Task(event_id, title, description, self.department)
        self.tasks.append(task)
        return task
    
    def assign_task(self, task: Task, workers: List[Worker]) -> None:
        if task.department != self.department:
            raise PermissionError("Cannot assign tasks outside your department.")
        
        for worker in workers:
            if worker.department != self.department:
                raise ValueError(f"{worker.name} is not in {self.department} department.")
            task.assigned_workers.append(worker)
            worker.tasks.append(task)
    
    def view_tasks(self) -> List[Task]:
        return self.tasks

    def change_task_status(self, task: Task, new_status: TaskStatus) -> None:
        if task.department != self.department:
            raise PermissionError("Cannot review tasks outside your department.")

        if new_status is task.status:
            raise ValueError("Cannot update task to same status.")

        task.status = new_status

    def review_feedback(self, task: Task) -> List[Comment]:
        if task.department != self.department:
            raise PermissionError("Cannot review tasks outside your department.")
        
        return task.comments

    def review_budget_requests(self, task: Task) -> List[BudgetRequest]:
        if task.department != self.department:
            raise PermissionError("Cannot review tasks outside your department.")
        
        return task.budget_requests

