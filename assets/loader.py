from __future__ import annotations

"""Utility for resolving asset file paths.

The :class:`AssetLoader` centralises access to resources bundled with the
project.  Paths are constructed relative to the ``assets`` directory at the
root of the repository.
"""

from pathlib import Path


class AssetLoader:
    """Resolve paths to various asset types.

    The loader defaults to using the directory containing this module as the
    root path but an alternative base can be supplied for testing.
    """

    def __init__(self, base: Path | None = None) -> None:
        self.base = Path(base or Path(__file__).resolve().parent)

    def path(self, *parts: str) -> Path:
        """Return a path inside the asset tree for the given parts."""
        return self.base.joinpath(*parts)

    def audio(self, filename: str) -> Path:
        """Return the path to an audio asset."""
        return self.path("audio", filename)

    def image(self, filename: str) -> Path:
        """Return the path to an image asset."""
        return self.path("images", filename)

    def font(self, filename: str) -> Path:
        """Return the path to a font asset."""
        return self.path("fonts", filename)
