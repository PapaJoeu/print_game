"""Player character with basic movement."""

from __future__ import annotations

import os
from typing import Tuple

import pygame

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "images")


class Player:
    """Simple player sprite controlled with WASD."""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        sprite_name: str = "player.png",
        speed: int = 5,
        bounds: Tuple[int, int] = (800, 600),
    ) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.bounds = bounds
        sprite_path = os.path.join(ASSETS_DIR, sprite_name)
        if os.path.exists(sprite_path):
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
        else:
            self.sprite = pygame.Surface((32, 32))
            self.sprite.fill((255, 0, 0))

    def handle_input(self) -> None:
        """Update position based on WASD keyboard input."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        self._clamp_to_bounds()

    def _clamp_to_bounds(self) -> None:
        """Keep the player within the map bounds."""
        max_x, max_y = self.bounds
        width, height = self.sprite.get_size()
        self.x = max(0, min(self.x, max_x - width))
        self.y = max(0, min(self.y, max_y - height))

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the sprite at its current position."""
        surface.blit(self.sprite, (self.x, self.y))
