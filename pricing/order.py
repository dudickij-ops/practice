"""Расчёт итоговой суммы заказа: позиции -> скидка -> налог -> округление."""

from decimal import Decimal, ROUND_HALF_UP

TAX_RATE = Decimal("0.20")
PROMO_RATE = Decimal("0.10")

LOYALTY_RATES = {
    "silver": Decimal("0.05"),
    "gold": Decimal("0.10"),
    "platinum": Decimal("0.15"),
}

MAX_DISCOUNT_RATE = Decimal("0.30")


def _money(value: Decimal) -> Decimal:
    """Округляет до копеек. Округление происходит ровно один раз, в самом конце."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def subtotal(items: list[dict]) -> Decimal:
    """Сумма позиций до скидок и налога."""
    total = Decimal("0")
    for item in items:
        total += Decimal(str(item["price"])) * Decimal(str(item["qty"]))
    return total


def discount_rate(customer: dict) -> Decimal:
    """Суммарная ставка скидки клиента, ограниченная сверху MAX_DISCOUNT_RATE."""
    rate = Decimal("0")

    if customer.get("promo_code"):
        rate += PROMO_RATE

    tier = customer.get("loyalty_tier")
    if tier:
        rate += LOYALTY_RATES[tier]

    return min(rate, MAX_DISCOUNT_RATE)


def order_total(items: list[dict], customer: dict) -> Decimal:
    """Итог к оплате: скидка на сумму позиций, затем налог, затем округление."""
    base = subtotal(items)

    discounted = base * (Decimal("1") - discount_rate(customer))

    tier = customer.get("loyalty_tier")
    if tier:
        discounted = discounted * (Decimal("1") - LOYALTY_RATES[tier])

    taxed = discounted * (Decimal("1") + TAX_RATE)
    return _money(taxed)
