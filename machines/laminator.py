from __future__ import annotations

from .base import Machine, MachineError


class Laminator(Machine):
    """Simple laminator that can run out of film."""

    def __init__(self, film_available: bool = True) -> None:
        super().__init__(name="Laminator")
        self.film_available = film_available

    def start_job(self, job: str) -> None:  # type: ignore[override]
        if not self.film_available:
            self.error("out of film")
        super().start_job(job)

