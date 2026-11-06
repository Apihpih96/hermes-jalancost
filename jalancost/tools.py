"""Hermes tool handler; the calculation itself lives in costing.py."""
import json

from .costing import calculate_trip_cost


def estimate_road_trip_cost(args: dict, **kwargs) -> str:
    """Return JSON for an input-only, offline road-trip estimate."""
    try:
        result = calculate_trip_cost(
            distance_km=args.get("distance_km"),
            trip_type=args.get("trip_type"),
            fuel_consumption_l_per_100km=args.get("fuel_consumption_l_per_100km"),
            fuel_price_myr_per_l=args.get("fuel_price_myr_per_l"),
            tolls_myr=args.get("tolls_myr"),
            passengers=args.get("passengers"),
        )
        return json.dumps({"ok": True, **result}, ensure_ascii=False)
    except Exception as exc:
        # Hermes handlers must return JSON for every input, never bubble up errors.
        return json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False)
