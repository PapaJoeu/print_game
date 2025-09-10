"""Pygame window rendering the print shop layout."""

from __future__ import annotations

import os
import pygame


ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "images")


class GameView:
    """Initialize a window and draw basic shop sprites."""

    def __init__(self, width: int = 800, height: int = 600, fps: int = 60) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Print Shop Simulator")
        self.clock = pygame.time.Clock()
        self.fps = fps

        # Load sprites
        floor_path = os.path.join(ASSETS_DIR, "floor.png")
        machine_path = os.path.join(ASSETS_DIR, "machine.png")
        self.floor = pygame.image.load(floor_path).convert_alpha()
        self.machine = pygame.image.load(machine_path).convert_alpha()

    def run(self) -> None:
        """Start the main loop rendering the shop each frame."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.floor, (0, 0))
            self.screen.blit(self.machine, (100, 100))
            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()


if __name__ == "__main__":
    GameView().run()
