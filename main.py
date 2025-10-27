from typing import List

class Task():
    def __init__(self, title: str, description: str, department: str) -> None:
        self.title: str = title
        self.description: str = description
        self.department: str = department
        self.assigned_workers: List[Worker] = []
        self.status: str = "Open"

    def __repr__(self) -> str:
        return f"<Task '{self.title}' ({self.status})>"

class Worker():
    def __init__(self, name: str, department: str, duty: str) -> None:
        self.name: str = name
        self.department: str = department
        self.duty: str = duty 
        self.tasks: List[Task] = []

    def view_tasks(self) -> List[Task]:
        return self.tasks

class Manager():
    def __init__(self, name: str, department: str) -> None:
        self.name: str = name
        self.department: str = department
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

def main():
    print("Hello from kth-id2207-project!")


if __name__ == "__main__":
    main()
