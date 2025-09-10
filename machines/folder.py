from __future__ import annotations

from .base import Machine, MachineError


class Folder(Machine):
    """Folding machine that may jam at a specified progress level."""

    def __init__(self, jam_at: int | None = None) -> None:
        super().__init__(name="Folder", locked=True)
        self.jam_at = jam_at

    def progress(self, amount: int) -> None:  # type: ignore[override]
        super().progress(amount)
        if self.jam_at is not None and self.progress_value >= self.jam_at:
            self.error("fold jam")

