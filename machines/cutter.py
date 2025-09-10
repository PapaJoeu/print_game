from __future__ import annotations

from .base import Machine, MachineError


class Cutter(Machine):
    """Large-scale cutter that stacks jobs of the same cut type.

    Each job specifies a ``cut_type`` and number of ``cuts``. Jobs with the
    same ``cut_type`` can be stacked together, sharing a single setup time and
    completing faster than running individually.
    """

    def __init__(self, time_per_cut: float = 1.0, setup_time: float = 2.0) -> None:
        super().__init__(name="Cutter", locked=True)
        self.time_per_cut = time_per_cut
        self.setup_time = setup_time
        self.current_cut_type: str | None = None
        self.jobs: list[str] = []
        self.total_cuts = 0
        self.time_spent = 0.0
        self.time_required = 0.0

    def start_job(self, job: str, cut_type: str, cuts: int) -> None:  # type: ignore[override]
        if self.job is None:
            self.current_cut_type = cut_type
            self.jobs = [job]
            self.total_cuts = cuts
            self.time_spent = 0.0
            self.time_required = self.setup_time + self.total_cuts * self.time_per_cut
            super().start_job(job)
        elif cut_type == self.current_cut_type:
            # Stack job with current batch
            self.jobs.append(job)
            self.total_cuts += cuts
            self.time_required = self.setup_time + self.total_cuts * self.time_per_cut
            self.job += f"+{job}"
        else:
            raise MachineError("different cut type in progress")

    def progress(self, time: float) -> None:  # type: ignore[override]
        if self.job is None:
            raise MachineError("No active job")
        self.time_spent += time
        ratio = self.time_spent / self.time_required if self.time_required else 0.0
        self.progress_value = min(100, int(ratio * 100))

    def complete(self) -> str:  # type: ignore[override]
        if self.job is None:
            raise MachineError("No active job")
        if self.progress_value < 100:
            self.error("cuts not finished")
        result = super().complete()
        # Reset for next batch
        self.current_cut_type = None
        self.jobs = []
        self.total_cuts = 0
        self.time_spent = 0.0
        self.time_required = 0.0
        return result

