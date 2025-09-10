from collections import deque
from typing import Deque, List, Optional

from .customer import Customer
from audio import SoundEvent, sound_manager


class QueueManager:
    """Manages a line of customers waiting for service."""

    def __init__(self) -> None:
        self._queue: Deque[Customer] = deque()

    def add_customer(self, customer: Customer) -> None:
        """Add a new customer to the queue."""
        self._queue.append(customer)
        # ding the bell when a customer enters the shop
        sound_manager.play(SoundEvent.BELL, caption="customer entered")

    def list_customers(self) -> List[Customer]:
        """Return a snapshot list of customers currently in queue."""
        return list(self._queue)

    def tick(self, amount: int = 1) -> List[Customer]:
        """Advance time by reducing patience; return customers who walked out."""
        walked_out: List[Customer] = []
        for cust in list(self._queue):
            cust.decrement_patience(amount)
            if cust.walked_out:
                self._queue.remove(cust)
                walked_out.append(cust)
        return walked_out

    def pop_next(self) -> Optional[Customer]:
        """Retrieve the next customer in line."""
        if self._queue:
            return self._queue.popleft()
        return None

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self._queue)
