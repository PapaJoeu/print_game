"""Simple audio and captions system for the print shop simulation.

Provides a minimal interface to play sound events, toggle captions,
manage volume and expose a stub for future text-to-speech integration.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, List
from pathlib import Path

from assets.loader import AssetLoader

try:  # pragma: no cover - optional dependency
    from pygame import mixer
    mixer.init()  # type: ignore[attr-defined]
except Exception:  # pragma: no cover - pygame may be unavailable
    mixer = None  # type: ignore[assignment]


class SoundEvent(Enum):
    """Identifiers for the various sound events."""

    BELL = "bell"  # customer entry
    ALERT = "alert"  # printer finished
    TTS = "tts"  # placeholder for text-to-speech events


class SoundManager:
    """Manage playback of sound events and caption display."""

    def __init__(self, loader: AssetLoader | None = None) -> None:
        self.loader = loader or AssetLoader()
        self.volume: float = 1.0
        self.captions_enabled: bool = False
        self.history: List[SoundEvent] = []
        self.captions: List[str] = []
        self.sounds: Dict[SoundEvent, object] = {}
        # Map events to logical channels for independent volume/mute control
        self._event_channel = {
            SoundEvent.BELL: "effects",
            SoundEvent.ALERT: "effects",
            SoundEvent.TTS: "tts",
        }
        self.channel_volumes: Dict[str, float] = {"effects": 1.0, "tts": 1.0}
        self.muted_channels: set[str] = set()

    # --- volume controls -------------------------------------------------
    def set_volume(self, level: float) -> None:
        """Set master volume level between 0.0 and 1.0."""
        self.volume = min(1.0, max(0.0, level))

    def set_channel_volume(self, channel: str, level: float) -> None:
        """Set volume for a specific channel between 0.0 and 1.0."""
        self.channel_volumes[channel] = min(1.0, max(0.0, level))

    def mute_channel(self, channel: str, muted: bool = True) -> None:
        """Mute or unmute a channel."""
        if muted:
            self.muted_channels.add(channel)
        else:
            self.muted_channels.discard(channel)

    # --- caption controls ------------------------------------------------
    def toggle_captions(self, enabled: bool) -> None:
        """Enable or disable caption display."""
        self.captions_enabled = enabled

    # --- playback --------------------------------------------------------
    def _resolve_sound(self, event: SoundEvent) -> Path:
        """Return the file path for a given sound event."""
        mapping = {
            SoundEvent.BELL: "bell.wav",
            SoundEvent.ALERT: "alert.wav",
            SoundEvent.TTS: "tts.wav",
        }
        return self.loader.audio(mapping[event])

    def load(self, event: SoundEvent) -> None:
        """Load a sound file for the given event using :mod:`pygame.mixer`."""
        if mixer is None or event in self.sounds:
            return
        path = self._resolve_sound(event)
        try:
            self.sounds[event] = mixer.Sound(str(path))  # type: ignore[attr-defined]
        except Exception:
            # Loading failures shouldn't crash the game; keep as unresolved.
            pass

    def load_all(self) -> None:
        """Preload all known sound events."""
        for event in SoundEvent:
            self.load(event)

    def play(self, event: SoundEvent, caption: str | None = None) -> None:
        """Record a sound event and optionally show a caption."""
        # Ensure the asset path is resolved for all consumers
        _path = self._resolve_sound(event)
        self.load(event)

        channel = self._event_channel.get(event, "effects")
        if channel not in self.muted_channels:
            sound = self.sounds.get(event)
            if sound is not None and mixer is not None:
                vol = self.volume * self.channel_volumes.get(channel, 1.0)
                try:
                    sound.set_volume(vol)
                except Exception:
                    pass
                try:
                    sound.play()
                except Exception:
                    pass

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
