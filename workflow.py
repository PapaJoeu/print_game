from customer import Customer


class Station:
    """Represents a workstation that can process a job."""

    def process(self, request_type: str) -> str:
        return f"Processed {request_type}"


def greet(customer: Customer) -> None:
    customer.satisfaction += 1


def process_job(customer: Customer, station: Station) -> None:
    station.process(customer.request_type)
    customer.satisfaction += 1


def deliver(customer: Customer) -> None:
    customer.satisfaction += 1


def checkout(customer: Customer) -> None:
    customer.satisfaction += 1


def run_workflow(customer: Customer, station: Station) -> None:
    """Run the full workflow for a single customer."""
    greet(customer)
    process_job(customer, station)
    deliver(customer)
    checkout(customer)
