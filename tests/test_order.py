from decimal import Decimal

from pricing import discount_rate, order_total, subtotal


def test_subtotal_sums_positions():
    items = [{"price": "10.00", "qty": 2}, {"price": "5.50", "qty": 4}]
    assert subtotal(items) == Decimal("42.00")


def test_subtotal_of_empty_cart_is_zero():
    assert subtotal([]) == Decimal("0")


def test_discount_rate_without_customer_data():
    assert discount_rate({}) == Decimal("0")


def test_discount_rate_promo_only():
    assert discount_rate({"promo_code": "SPRING"}) == Decimal("0.10")


def test_discount_rate_silver_tier():
    assert discount_rate({"loyalty_tier": "silver"}) == Decimal("0.05")


def test_discount_rate_gold_tier():
    assert discount_rate({"loyalty_tier": "gold"}) == Decimal("0.10")


def test_discount_rate_promo_plus_tier_sums():
    customer = {"promo_code": "SPRING", "loyalty_tier": "platinum"}
    assert discount_rate(customer) == Decimal("0.25")


def test_order_total_without_discounts_applies_tax():
    items = [{"price": "100.00", "qty": 1}]
    assert order_total(items, {}) == Decimal("120.00")


def test_order_total_with_promo_code():
    items = [{"price": "100.00", "qty": 1}]
    assert order_total(items, {"promo_code": "SPRING"}) == Decimal("108.00")


def test_order_total_rounds_once_at_the_end():
    items = [{"price": "9.99", "qty": 3}]
    assert order_total(items, {}) == Decimal("35.96")


def test_order_total_of_empty_cart_is_zero():
    assert order_total([], {"promo_code": "SPRING"}) == Decimal("0.00")
