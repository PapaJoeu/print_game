from __future__ import annotations

"""Command line interface for the print shop simulation.

The module exposes a :class:`Game` class which wires together the queue,
machines and tutorial systems.  When run as a script it provides a tiny
interactive shell so the module can be exercised from the command line.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from customers.customer import Customer
from customers.queue import QueueManager
from machines import Binder, Machine, Printer
from tutorial import Tutorial, default_tutorial


@dataclass
class Game:
    """Light‑weight container object holding the game state.

    The game tracks a queue of customers, a collection of spawned machines and
    the active tutorial sequence.  Machines can be spawned dynamically and when
    both a printer and binder exist the default tutorial is started
    automatically.
    """

    queue: QueueManager = QueueManager()
    machines: Dict[str, Machine] = None  # type: ignore[assignment]
    tutorial: Optional[Tutorial] = None

    def __post_init__(self) -> None:
        self.machines = {}

    # ------------------------------------------------------------------
    # State management helpers
    def spawn_machine(self, machine: Machine) -> Machine:
        """Add a machine to the shop and start the tutorial if possible."""
        self.machines[machine.name.lower()] = machine
        if {"printer", "binder"} <= set(self.machines) and self.tutorial is None:
            self.tutorial = default_tutorial(
                self.machines["printer"], self.machines["binder"]
            )
            self.tutorial.start()
        return machine

    def add_customer(self, request_type: str, patience: int) -> Customer:
        """Create and enqueue a new :class:`Customer`."""
        customer = Customer(request_type, patience)
        self.queue.add_customer(customer)
        return customer

    def assign_next_customer(self, machine_name: str) -> Optional[Customer]:
        """Assign the next customer in queue to ``machine_name``.

        The customer's ``request_type`` is used as the job identifier for the
        machine.  ``None`` is returned if the queue is empty.
        """
        machine = self.machines[machine_name]
        customer = self.queue.pop_next()
        if customer:
            machine.start_job(customer.request_type)
        return customer

    def progress_jobs(self, amount: int) -> List[str]:
        """Advance all active machine jobs by ``amount`` percent.

        Completed job identifiers are returned.  The queue patience is ticked to
        simulate time passing.
        """
        completed: List[str] = []
        for machine in self.machines.values():
            if machine.job is None:
                continue
            if isinstance(machine, Binder):
                # binder expects a spine width measurement; use its target width
                machine.progress(machine.target_width)
            else:
                machine.progress(amount)
            if machine.progress_value >= 100:
                completed.append(machine.complete())
        # customers waiting lose a little patience as time progresses
        self.queue.tick()
        return completed


# ----------------------------------------------------------------------
# Command line interface

def main() -> None:  # pragma: no cover - exercised via CLI example
    game = Game()
    print("Print Shop interactive shell. Commands: spawn <printer|binder>, add <type> <patience>, process <machine>, progress <amount>, quit")
    while True:
        try:
            parts = input("> ").split()
        except EOFError:
            print()
            break
        if not parts:
            continue
        cmd = parts[0].lower()
        if cmd == "spawn" and len(parts) >= 2:
            typ = parts[1].lower()
            if typ == "printer":
                game.spawn_machine(Printer())
                print("Spawned printer")
            elif typ == "binder":
                game.spawn_machine(Binder())
                print("Spawned binder")
            else:
                print("Unknown machine")
        elif cmd == "add" and len(parts) >= 3:
            req = parts[1]
            patience = int(parts[2])
            game.add_customer(req, patience)
            print("Customer added")
        elif cmd == "process" and len(parts) >= 2:
            machine_name = parts[1].lower()
            cust = game.assign_next_customer(machine_name)
            if cust:
                print(f"Started {cust.request_type} on {machine_name}")
            else:
                print("No customers in queue")
        elif cmd == "progress" and len(parts) >= 2:
            amount = int(parts[1])
            for job in game.progress_jobs(amount):
                print(f"Completed {job}")
        elif cmd in {"quit", "exit"}:
            break
        else:
            print("Unknown command")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
