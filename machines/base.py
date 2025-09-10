from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


class MachineError(Exception):
    """Raised when a machine encounters an error."""


@dataclass
class Machine:
    """Base class for print shop machines.

    Provides hooks for starting a job, tracking progress and completing a job.
    Concrete machines should trigger cues on completion or error.
    """

    name: str
    progress_value: int = 0
    job: Optional[str] = None
    cues: List[str] = field(default_factory=list)

    def start_job(self, job: str) -> None:
        """Begin processing a new job."""
        self.job = job
        self.progress_value = 0
        self.cues.clear()
        self.trigger_cue("visual: start")
        self.trigger_cue("audio: start")

    def progress(self, amount: int) -> None:
        """Advance the job by ``amount`` percent."""
        if self.job is None:
            raise MachineError("No active job")
        self.progress_value = min(100, self.progress_value + amount)

    def complete(self) -> str:
        """Mark the current job as complete and emit cues."""
        if self.job is None:
            raise MachineError("No active job")
        self.trigger_cue("visual: complete")
        self.trigger_cue("audio: complete")
        job = self.job
        self.job = None
        return job

    def error(self, reason: str) -> None:
        """Abort the current job and emit error cues."""
        self.trigger_cue(f"visual: error {reason}")
        self.trigger_cue(f"audio: error {reason}")
        self.job = None
        raise MachineError(reason)

    def trigger_cue(self, cue: str) -> None:
        """Record a visual or audio cue."""
        self.cues.append(cue)
