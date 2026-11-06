"""Pure deterministic calculation for user-entered road-trip assumptions."""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Any


class InputError(ValueError):
    """Raised when an input cannot safely produce a meaningful estimate."""


def _decimal(value: Any, field: str) -> Decimal:
    if isinstance(value, bool) or value is None:
        raise InputError(f"{field} must be a finite number")
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise InputError(f"{field} must be a finite number") from None
    if not number.is_finite():
        raise InputError(f"{field} must be a finite number")
    return number


def _money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _fixed(value: Decimal, places: str) -> str:
    return format(value.quantize(Decimal(places), rounding=ROUND_HALF_UP), "f")


def calculate_trip_cost(
    *,
    distance_km: Any,
    trip_type: Any,
    fuel_consumption_l_per_100km: Any,
    fuel_price_myr_per_l: Any,
    tolls_myr: Any = None,
    passengers: Any,
) -> dict[str, Any]:
    """Return costs from provided values only; tolls are total for the journey.

    ``distance_km`` is always one-way distance. When tolls are None, the
    returned total is explicitly a fuel-only known-cost estimate.
    """
    distance = _decimal(distance_km, "distance_km")
    consumption = _decimal(fuel_consumption_l_per_100km, "fuel_consumption_l_per_100km")
    price = _decimal(fuel_price_myr_per_l, "fuel_price_myr_per_l")

    if distance <= 0:
        raise InputError("distance_km must be greater than zero")
    if consumption <= 0:
        raise InputError("fuel_consumption_l_per_100km must be greater than zero")
    if price < 0:
        raise InputError("fuel_price_myr_per_l cannot be negative")
    if trip_type not in ("one_way", "round_trip"):
        raise InputError("trip_type must be one_way or round_trip")
    if isinstance(passengers, bool) or not isinstance(passengers, int) or passengers < 1:
        raise InputError("passengers must be a positive integer")

    if tolls_myr is None:
        tolls = None
    else:
        tolls = _decimal(tolls_myr, "tolls_myr")
        if tolls < 0:
            raise InputError("tolls_myr cannot be negative")
        tolls = _money(tolls)

    multiplier = Decimal(2) if trip_type == "round_trip" else Decimal(1)
    trip_distance = distance * multiplier
    litres = (trip_distance * consumption / Decimal(100)).quantize(
        Decimal("0.001"), rounding=ROUND_HALF_UP
    )
    fuel_cost = _money(litres * price)
    total_known_cost = fuel_cost if tolls is None else _money(fuel_cost + tolls)
    per_person = _money(total_known_cost / Decimal(passengers))

    return {
        "trip_type": trip_type,
        "distance_km": _fixed(trip_distance, "0.01"),
        "fuel_liters_estimate": _fixed(litres, "0.001"),
        "fuel_cost_myr": _fixed(fuel_cost, "0.01"),
        "tolls_myr": None if tolls is None else _fixed(tolls, "0.01"),
        "tolls_included": tolls is not None,
        "total_known_cost_myr": _fixed(total_known_cost, "0.01"),
        "per_person_known_cost_myr": _fixed(per_person, "0.01"),
        "passengers": passengers,
        "note": (
            "Estimate uses only the supplied inputs; no live fuel-price, route, "
            "traffic, or toll data is fetched."
            if tolls is not None
            else "Fuel-only estimate: tolls were not supplied, so they are excluded. "
            "No live fuel-price, route, traffic, or toll data is fetched."
        ),
    }
