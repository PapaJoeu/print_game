from customers.customer import Customer
from workflow import Station, run_workflow


def test_run_workflow_increases_satisfaction():
    customer = Customer("scan", patience=3)
    station = Station()
    run_workflow(customer, station)
    assert customer.satisfaction == 4
