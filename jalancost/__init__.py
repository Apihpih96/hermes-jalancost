"""JalanCost: deterministic, offline road-trip cost estimates."""
from . import schemas, tools


def register(ctx):
    """Register the public estimate tool; no network or privileged host access."""
    ctx.register_tool(
        name="estimate_road_trip_cost",
        toolset="jalancost",
        schema=schemas.ESTIMATE_ROAD_TRIP_COST,
        handler=tools.estimate_road_trip_cost,
    )
