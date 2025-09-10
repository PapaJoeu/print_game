from __future__ import annotations

from .base import Machine, MachineError


class Printer(Machine):
    """Simulates a printer with potential jams or paper shortages."""

    def __init__(self, paper_available: bool = True, jam_at: int | None = None) -> None:
        super().__init__(name="Printer")
        self.paper_available = paper_available
        self.jam_at = jam_at

    def start_job(self, job: str) -> None:  # type: ignore[override]
        if not self.paper_available:
            self.error("out of paper")
        super().start_job(job)

    def progress(self, amount: int) -> None:  # type: ignore[override]
        super().progress(amount)
        if self.jam_at is not None and self.progress_value >= self.jam_at:
            self.error("paper jam")
