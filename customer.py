from dataclasses import dataclass


@dataclass
class Customer:
    """Represents a customer waiting for service."""

    request_type: str
    patience: int
    satisfaction: int = 0

    def decrement_patience(self, amount: int = 1) -> int:
        """Decrease patience by ``amount`` and return remaining patience."""
        self.patience = max(0, self.patience - amount)
        return self.patience

    @property
    def walked_out(self) -> bool:
        """Whether the customer has left the queue due to zero patience."""
        return self.patience == 0
