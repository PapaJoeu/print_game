"""Customer classes for the print shop simulation.

This module now contains multiple customer archetypes used by the tests.
Each subtype has its own flavour of patience behaviour or interaction. The
base :class:`Customer` also supports a ``assist`` method allowing one customer
to temporarily help another, representing the optional "delegate" mechanic.
"""

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

    def assist(self, other: "Customer") -> None:
        """Temporarily help another customer.

        The helper loses a unit of patience for the time spent but both
        customers gain a point of satisfaction.
        """

        self.decrement_patience()
        self.satisfaction += 1
        other.satisfaction += 1

    @property
    def walked_out(self) -> bool:
        """Whether the customer has left the queue due to zero patience."""
        return self.patience == 0


@dataclass
class AverageCustomer(Customer):
    """Standard customer with no special behaviour."""


@dataclass
class ElderlyCustomer(Customer):
    """Elderly customer who loses patience more slowly."""

    def decrement_patience(self, amount: int = 1) -> int:
        """Half-speed patience decay (rounded down, minimum of one)."""

        reduction = max(1, amount // 2)
        return super().decrement_patience(reduction)


@dataclass
class RushedCustomer(Customer):
    """Businessperson with rapid patience decay."""

    def decrement_patience(self, amount: int = 1) -> int:
        """Patience decays twice as fast."""

        return super().decrement_patience(amount * 2)


@dataclass
class DIYCustomer(Customer):
    """DIY customer who will call for help if a jam occurs."""

    called_for_help: bool = False

    def handle_jam(self) -> None:
        """Simulate encountering a printer jam and requesting help."""

        self.called_for_help = True
