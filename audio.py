"""Simple audio and captions system for the print shop simulation.

Provides a minimal interface to play sound events, toggle captions,
manage volume and expose a stub for future text-to-speech integration.
"""

from __future__ import annotations

from enum import Enum
from typing import List


class SoundEvent(Enum):
    """Identifiers for the various sound events."""

    BELL = "bell"  # customer entry
    ALERT = "alert"  # printer finished
    TTS = "tts"  # placeholder for text-to-speech events


class SoundManager:
    """Manage playback of sound events and caption display."""

    def __init__(self) -> None:
        self.volume: float = 1.0
        self.captions_enabled: bool = False
        self.history: List[SoundEvent] = []
        self.captions: List[str] = []

    # --- volume controls -------------------------------------------------
    def set_volume(self, level: float) -> None:
        """Set master volume level between 0.0 and 1.0."""
        self.volume = min(1.0, max(0.0, level))

    # --- caption controls ------------------------------------------------
    def toggle_captions(self, enabled: bool) -> None:
        """Enable or disable caption display."""
        self.captions_enabled = enabled

    # --- playback --------------------------------------------------------
    def play(self, event: SoundEvent, caption: str | None = None) -> None:
        """Record a sound event and optionally show a caption."""
        self.history.append(event)
        if self.captions_enabled and caption:
            self.captions.append(caption)

    # --- text to speech --------------------------------------------------
    def speak(self, text: str) -> None:
        """Placeholder method for future text-to-speech integration."""
        # For now we simply log the event and optionally show a caption.
        self.history.append(SoundEvent.TTS)
        if self.captions_enabled:
            self.captions.append(text)


# Global sound manager instance used across the game.
sound_manager = SoundManager()
