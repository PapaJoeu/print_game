from customers.customer import (
    AverageCustomer,
    Customer,
    DIYCustomer,
    ElderlyCustomer,
    RushedCustomer,
)


def test_customer_patience_decrements_and_walkout():
    customer = Customer("copy", patience=2)
    customer.decrement_patience()
    assert customer.patience == 1
    assert not customer.walked_out
    customer.decrement_patience()
    assert customer.walked_out


def test_rushed_customer_patience_decay_faster():
    cust = RushedCustomer("print", patience=5)
    cust.decrement_patience()
    assert cust.patience == 3


def test_elderly_customer_patience_decay_slower():
    cust = ElderlyCustomer("print", patience=5)
    cust.decrement_patience(2)
    assert cust.patience == 4


def test_diy_customer_calls_for_help_on_jam():
    cust = DIYCustomer("print", patience=5)
    cust.handle_jam()
    assert cust.called_for_help


def test_delegate_interaction():
    helper = AverageCustomer("scan", patience=3)
    recipient = AverageCustomer("copy", patience=3)
    helper.assist(recipient)
    assert helper.patience == 2
    assert helper.satisfaction == 1
    assert recipient.satisfaction == 1
