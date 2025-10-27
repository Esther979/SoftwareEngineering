from typing import List, Dict

class Employee():
    def __init__(self, name: str, department: str) -> None:
        self.name = name
        self.department = department

class Task():
    def __init__(self, title: str, description: str, department: str) -> None:
        self.title: str = title
        self.description: str = description
        self.department: str = department
        self.assigned_workers: List[Worker] = []
        self.status: str = "Open"
        self.comments: List[Dict[str, str]] = []

    def add_comment(self, worker_name: str, comment: str) -> None:
        self.comments.append({"worker": worker_name, "comment": comment})

    def __repr__(self) -> str:
        return f"<Task '{self.title}' ({self.status})>"

class Worker(Employee):
    def __init__(self, name: str, department: str, duty: str) -> None:
        super().__init__(name, department)
        self.duty: str = duty 
        self.tasks: List[Task] = []

    def view_tasks(self) -> List[Task]:
        return self.tasks

    def comment_on_task(self, task: Task, comment: str) -> None:
        if task not in self.tasks:
            raise PermissionError("You are not assigned to this task.")

        task.add_comment(self.name, comment)

class Manager(Employee):
    def __init__(self, name: str, department: str) -> None:
        super().__init__(name, department)
        self.tasks: List[Task] = []
    
    def create_task(self, title: str, description: str) -> Task:
        task = Task(title, description, self.department)
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

    def review_feedback(self, task: Task) -> List[Dict[str, str]]:
        if task.department != self.department:
            raise PermissionError("Cannot review tasks outside your department.")
        
        return task.comments

