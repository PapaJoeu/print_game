"""Heads-up display components for the print shop simulation."""

from __future__ import annotations

from typing import Iterable, List

from machines.base import Machine
from queue_manager import QueueManager


class QueueDisplay:
    """Simple text-based queue display."""

    def render(self, queue: QueueManager) -> List[str]:
        """Return a list of customer request types in order."""
        return [cust.request_type for cust in queue.list_customers()]


class MachineStatusPanel:
    """Display status information for a machine."""

    def render(self, machine: Machine) -> str:
        job = machine.job or "idle"
        return f"{machine.name}: {job} ({machine.progress_value}%)"


class JobHUD:
    """Track and display the workflow steps for a job."""

    steps: Iterable[str] = ("greet", "process_job", "deliver", "checkout")

    def __init__(self) -> None:
        self.completed: List[str] = []

    def mark_complete(self, step: str) -> None:
        """Mark a workflow step as completed."""
        if step in self.steps and step not in self.completed:
            self.completed.append(step)

    def render(self) -> List[str]:
        """Return a checklist style representation of the workflow."""
        return [
            ("[x] " + step) if step in self.completed else ("[ ] " + step)
            for step in self.steps
        ]
