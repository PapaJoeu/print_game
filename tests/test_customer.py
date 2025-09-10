from customer import Customer


def test_customer_patience_decrements_and_walkout():
    customer = Customer("copy", patience=2)
    customer.decrement_patience()
    assert customer.patience == 1
    assert not customer.walked_out
    customer.decrement_patience()
    assert customer.walked_out
