"""Pause menu with access to the replayable tutorial."""
from __future__ import annotations

from typing import Optional

from tutorial import Tutorial, TutorialStep


class PauseMenu:
    """Represents a very small pause menu.

    The menu exposes a :meth:`replay_tutorial` method which resets and restarts
    the provided :class:`Tutorial`.  The method returns the first
    :class:`TutorialStep` so callers can immediately display the opening
    instruction again.
    """

    def __init__(self, tutorial: Tutorial) -> None:
        self.tutorial = tutorial

    def replay_tutorial(self) -> Optional[TutorialStep]:
        """Restart the tutorial from the beginning."""
        self.tutorial.reset()
        if self.tutorial.steps:
            return self.tutorial.start()
        return None
