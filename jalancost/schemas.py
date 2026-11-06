"""Tool schema shown to Hermes."""

ESTIMATE_ROAD_TRIP_COST = {
    "name": "estimate_road_trip_cost",
    "description": (
        "Estimate Malaysian ringgit fuel and known toll costs for a one-way or "
        "round-trip road journey using only the supplied distance, vehicle fuel "
        "consumption, fuel price, toll amount, and passenger count. Do not use "
        "for live route, traffic, fuel-price, or toll lookups. The distance is "
        "one-way; tolls are the total for the selected journey."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "distance_km": {
                "type": "number",
                "exclusiveMinimum": 0,
                "description": "One-way road distance in kilometres, supplied by the user.",
            },
            "trip_type": {
                "type": "string",
                "enum": ["one_way", "round_trip"],
                "description": "Whether to estimate one-way or return travel.",
            },
            "fuel_consumption_l_per_100km": {
                "type": "number",
                "exclusiveMinimum": 0,
                "description": "Vehicle fuel consumption in litres per 100 km, supplied by the user.",
            },
            "fuel_price_myr_per_l": {
                "type": "number",
                "minimum": 0,
                "description": "Fuel price in MYR per litre, supplied by the user; never assume a current price.",
            },
            "tolls_myr": {
                "type": ["number", "null"],
                "minimum": 0,
                "description": "Optional total toll amount in MYR for the selected journey. Null or omitted means tolls are excluded from the total.",
            },
            "passengers": {
                "type": "integer",
                "minimum": 1,
                "description": "Number of people sharing the known trip cost.",
            },
        },
        "required": [
            "distance_km",
            "trip_type",
            "fuel_consumption_l_per_100km",
            "fuel_price_myr_per_l",
            "passengers",
        ],
        "additionalProperties": False,
    },
}
