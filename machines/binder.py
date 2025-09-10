from __future__ import annotations

from .base import Machine, MachineError


class Binder(Machine):
    """Binding machine where players input the correct spine measurement."""

    def __init__(self, target_width: float = 1.0, tolerance: float = 0.05) -> None:
        super().__init__(name="Binder")
        self.target_width = target_width
        self.tolerance = tolerance
        self._success: bool | None = None

    def start_job(self, job: str) -> None:  # type: ignore[override]
        super().start_job(job)
        self._success = None

    def progress(self, measurement: float) -> None:  # type: ignore[override]
        """Player inputs the measured spine width for binding."""
        if self.job is None:
            raise MachineError("No active job")
        self._success = abs(measurement - self.target_width) <= self.tolerance
        self.progress_value = 100

    def complete(self) -> str:  # type: ignore[override]
        if self.job is None:
            raise MachineError("No active job")
        if not self._success:
            self.error("binding failed")
        return super().complete()
