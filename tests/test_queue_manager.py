from customers.customer import Customer
from customers.queue import QueueManager


def test_queue_manager_walk_out():
    manager = QueueManager()
    cust = Customer("print", patience=1)
    manager.add_customer(cust)
    walked_out = manager.tick()
    assert walked_out == [cust]
    assert len(manager) == 0
