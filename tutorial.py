"""Simple step-by-step tutorial system for the print shop game.

The tutorial guides the player through the first few jobs by presenting
instructions that include the relevant control input and workstation.  Advanced
machines remain locked until a step that references them becomes active.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from machines.base import Machine


@dataclass
class TutorialStep:
    """A single step in the tutorial sequence."""

    instruction: str
    control: str
    station: str
    machine: Optional[Machine] = None


class Tutorial:
    """Manage a sequence of :class:`TutorialStep` objects.

    The tutorial can be started, advanced through steps and reset in order to be
    replayed.  When a step becomes active any associated machine is unlocked so
    that it may be used.
    """

    def __init__(self, steps: List[TutorialStep]) -> None:
        self.steps = steps
        self.index = 0
        self.active = False

    def start(self) -> TutorialStep:
        """Begin the tutorial and return the first step."""
        self.active = True
        self.index = 0
        return self.current_step()

    def current_step(self) -> TutorialStep:
        """Return the currently active step and unlock its machine."""
        step = self.steps[self.index]
        if step.machine:
            step.machine.unlock()
        return step

    def next_step(self) -> Optional[TutorialStep]:
        """Advance to the next step and return it.

        Returns ``None`` when the tutorial has been completed.
        """
        if not self.active:
            return self.start()
        self.index += 1
        if self.index >= len(self.steps):
            self.active = False
            return None
        return self.current_step()

    def reset(self) -> None:
        """Reset the tutorial so it can be replayed.

        Any machines referenced by steps are locked again so the tutorial can
        guide the player from the start on subsequent playthroughs.
        """
        for step in self.steps:
            if step.machine:
                step.machine.lock()
        self.index = 0
        self.active = False

    def is_complete(self) -> bool:
        """Whether all steps have been completed."""
        return not self.active and self.index >= len(self.steps)


def default_tutorial(printer: Machine, binder: Machine) -> Tutorial:
    """Create a basic tutorial for the first jobs.

    Parameters
    ----------
    printer, binder:
        Machine instances used in the tutorial.  The binder is expected to be
        locked and will be unlocked when its step becomes active.
    """

    steps = [
        TutorialStep("Approach the printer", "WASD", "Printer", printer),
        TutorialStep("Start the print job", "E", "Printer"),
        TutorialStep("Carry prints to the binder", "WASD", "Binder", binder),
        TutorialStep("Bind the booklet", "E", "Binder"),
    ]
    return Tutorial(steps)
