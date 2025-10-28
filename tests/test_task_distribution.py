import unittest
from typing import List
from src.workflow import Task, Manager, Worker, Department, TaskStatus, Comment, BudgetRequest

class TestTaskWorkflow(unittest.TestCase):
    def setUp(self) -> None:
        """Set up a manager and a few workers for each test."""
        self.manager: Manager = Manager("Jack", Department.PRODUCTION)
        self.workers: List[Worker] = [
            Worker("Tobias", Department.PRODUCTION, "Photographer"),
            Worker("Antony", Department.PRODUCTION, "Audio Specialist"),
            Worker("Adam", Department.PRODUCTION, "Audio Specialist")
        ]

    def test_manager_can_create_task(self) -> None:
        """Managers should be able to create tasks for their department."""
        task = self.manager.create_task("Prepare Stage", "Set up stage lightning and decorations.")

        self.assertIsInstance(task, Task)
        self.assertIn(task, self.manager.tasks)
        self.assertEqual(task.department, self.manager.department)
        self.assertEqual(task.status, TaskStatus.OPEN)
    
    def test_manager_can_assign_task_to_department_workers(self) -> None:
        """Managers can assign tasks to workers in the same department."""
        task = self.manager.create_task("Prepare Stage", "Set up stage lightning and decorations.")
        self.manager.assign_task(task, self.workers)

        for worker in self.workers:
            self.assertIn(task, worker.tasks)
            self.assertIn(worker, task.assigned_workers)

    def test_manager_cannot_assign_task_outside_department(self) -> None:
        """Managers cannot assign task to workers from another department."""
        outsider: Worker = Worker("Helen", Department.SERVICES, "Top Chef")
        task = self.manager.create_task("Prepare Stage", "Set up stage lightning and decorations.")

        with self.assertRaises(ValueError):
            self.manager.assign_task(task, [outsider])

    def test_manager_can_update_task_status(self) -> None:
        """Managers can change task status within valid transitions."""
        task = self.manager.create_task("Prepare Stage", "Set up stage lightning and decorations.")

        self.manager.change_task_status(task, TaskStatus.IN_PROGRESS)
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)

        self.manager.change_task_status(task, TaskStatus.CLOSED)
        self.assertEqual(task.status, TaskStatus.CLOSED)

    def test_invalid_status_transitions_raises_error(self) -> None:
        """Managers cannot make invalid task status transitions."""
        task = self.manager.create_task("Prepare Stage", "Set up stage lightning and decorations.")

        with self.assertRaises(ValueError):
            self.manager.change_task_status(task, TaskStatus.OPEN)

    def test_manager_can_review_feedback_on_task(self) -> None:
        """Manager can review comments left by workers on a task."""
        task = self.manager.create_task("Prepare Stage", "Set up stage lightning and decorations.")
        self.manager.assign_task(task, [self.workers[0]])

        self.workers[0].comment_on_task(task, "We'll use neon lights.")
        feedback: List[Comment] = self.manager.review_feedback(task)

        self.assertEqual(feedback, task.comments)

    def test_manager_can_review_budget_requests_on_task(self) -> None:
        """Manager can review budget adjustments requested by workers on a task."""
        task = self.manager.create_task("Prepare Stage", "Set up stage lightning and decorations.")
        self.manager.assign_task(task, [self.workers[0]])

        self.workers[0].request_more_budget(task, 25000, "We'll have to rent a roof and lightning grid.")
        budget_request: List[BudgetRequest] = self.manager.review_budget_requests(task)
        
        self.assertEqual(budget_request, task.budget_requests)

    def test_worker_initially_has_no_tasks(self) -> None:
        """A newly created worker should have no tasks assigned."""
        new_worker: Worker = Worker("Parache", Department.PRODUCTION, "IT Specialist")
        self.assertEqual(len(new_worker.view_tasks()), 0)

    def test_worker_can_view_assigned_tasks(self) -> None:
        """Workers should see tasks assigned to them."""
        task = self.manager.create_task("Prepare Stage", "Set up stage lightning and decorations.")
        self.manager.assign_task(task, [self.workers[0]])
        worker_tasks: List[Task] = self.workers[0].view_tasks()
        self.assertIn(task, worker_tasks)

    def test_worker_can_comment_on_task(self) -> None:
        """Workers can add comment to tasks assigned to them."""
        task = self.manager.create_task("Prepare Stage", "Set up stage lightning and decorations.")
        self.manager.assign_task(task, [self.workers[0]])

        self.workers[0].comment_on_task(task, "We'll use neon lights.")
        comments = task.comments

        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0]["worker"], "Tobias")
        self.assertEqual(comments[0]["comment"], "We'll use neon lights.")

    def test_worker_cannot_comment_on_unassigned_task(self) -> None:
        """Workers cannot add a comment to tasks that are not assigned to them."""
        task = self.manager.create_task("Prepare Stage", "Set up stage lightning and decorations.")
        self.manager.assign_task(task, [self.workers[0]])

        with self.assertRaises(PermissionError):
            self.workers[1].comment_on_task(task, "We'll use neon lights.")

    def test_worker_can_request_additional_budget_on_task(self) -> None:
        """Workers can request additional budget on tasks assigned to them."""
        task = self.manager.create_task("Prepare Stage", "Set up stage lightning and decorations.")
        self.manager.assign_task(task, [self.workers[0]])

        self.workers[0].request_more_budget(task, 25000, "We'll have to rent a roof and lightning grid.")
        budget_requests = task.budget_requests

        self.assertEqual(len(budget_requests), 1)
        self.assertEqual(budget_requests[0]["worker"], "Tobias")
        self.assertEqual(budget_requests[0]["amount"], 25000)
        self.assertEqual(budget_requests[0]["reason"], "We'll have to rent a roof and lightning grid.")
        
    def test_worker_cannot_request_additional_budget_on_unassigned_task(self) -> None:
        """Workers cannot request additional budget on tasks that are not assigned to them."""
        task = self.manager.create_task("Prepare Stage", "Set up stage lightning and decorations.")
        self.manager.assign_task(task, [self.workers[0]])

        with self.assertRaises(PermissionError):
            self.workers[1].request_more_budget(task, 25000, "We'll have to rent a roof and lightning grid.")


if __name__ == "__main__":
    unittest.main()
