import unittest
from typing import List
from main import Task, Manager, Worker

class TestTaskWorkflow(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a manager and a few workers for each test."""
        self.manager: Manager = Manager("Jack", "Production")
        self.workers: List[Worker] = [
            Worker("Tobias", "Production", "Photographer"),
            Worker("Antony", "Production", "Audio Specialist"),
            Worker("Adam", "Production", "Audio Specialist")
        ]

    def test_manager_can_create_task(self) -> None:
        """Managers should be able to create tasks for their department."""
        task = self.manager.create_task("Prepare Stage", "Set up stage lightning and decorations.")

        self.assertIsInstance(task, Task)
        self.assertIn(task, self.manager.tasks)
        self.assertEqual(task.department, self.manager.department)
        self.assertEqual(task.status, "Open")
    
    def test_manager_can_assign_task_to_department_workers(self) -> None:
        """Managers can assign tasks to workers in the same department."""
        task = self.manager.create_task("Prepare Stage", "Set up stage lightning and decorations.")
        self.manager.assign_task(task, self.workers)

        for worker in self.workers:
            self.assertIn(task, worker.tasks)
            self.assertIn(worker, task.assigned_workers)

    def test_manager_cannot_assign_task_outside_department(self) -> None:
        """Managers cannot assign task to workers from another department."""
        outsider: Worker = Worker("Helen", "Services", "Top Chef")
        task = self.manager.create_task("Prepare Stage", "Set up stage lightning and decorations.")

        with self.assertRaises(ValueError):
            self.manager.assign_task(task, [outsider])

    def test_worker_can_view_assigned_tasks(self) -> None:
        """Workers should see tasks assigned to them."""
        task = self.manager.create_task("Prepare Stage", "Set up stage lightning and decorations.")
        self.manager.assign_task(task, [self.workers[0]])
        worker_tasks: List[Task] = self.workers[0].view_tasks()
        self.assertIn(task, worker_tasks)

    def test_worker_initially_has_no_tasks(self) -> None:
        """A newly created worker should have no tasks assigned."""
        new_worker: Worker = Worker("Parache", "Production", "IT Specialist")
        self.assertEqual(len(new_worker.view_tasks()), 0)

if __name__ == "__main__":
    unittest.main()
