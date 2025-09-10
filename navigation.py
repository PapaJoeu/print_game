"""Navigation utilities with keyboard hotkeys and pathfinding."""

from __future__ import annotations

from collections import deque
from enum import Enum
from typing import Callable, Dict, Iterable, List


class HotkeyManager:
    """Register and trigger actions via keyboard hotkeys."""

    def __init__(self) -> None:
        self._actions: Dict[str, Callable[..., object]] = {}

    def register(self, key: str, action: Callable[..., object]) -> None:
        self._actions[key] = action

    def trigger(self, key: str, *args, **kwargs) -> object:
        if key not in self._actions:
            raise KeyError(f"No action bound for {key}")
        return self._actions[key](*args, **kwargs)


class NavigationMode(Enum):
    PATHFINDING = "pathfinding"
    INSTANT = "instant"


class Navigator:
    """Select stations using either pathfinding or instant travel."""

    def __init__(self, graph: Dict[str, Iterable[str]], mode: NavigationMode = NavigationMode.PATHFINDING) -> None:
        self.graph = graph
        self.mode = mode

    def select_station(self, start: str, target: str) -> List[str]:
        """Return path to ``target`` based on navigation mode."""
        if self.mode is NavigationMode.INSTANT:
            return [target]
        return self._bfs_path(start, target)

    def _bfs_path(self, start: str, target: str) -> List[str]:
        queue = deque([(start, [start])])
        visited = {start}
        while queue:
            node, path = queue.popleft()
            if node == target:
                return path
            for neighbour in self.graph.get(node, []):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append((neighbour, path + [neighbour]))
        return []
