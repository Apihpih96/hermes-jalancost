import json
import unittest

from jalancost.costing import InputError, calculate_trip_cost
from jalancost.tools import estimate_road_trip_cost


class TripCostTests(unittest.TestCase):
    def test_round_trip_fuel_toll_and_split(self):
        result = calculate_trip_cost(
            distance_km=100,
            trip_type="round_trip",
            fuel_consumption_l_per_100km=8,
            fuel_price_myr_per_l=2.05,
            tolls_myr=10,
            passengers=4,
        )
        self.assertEqual(result["distance_km"], "200.00")
        self.assertEqual(result["fuel_liters_estimate"], "16.000")
        self.assertEqual(result["fuel_cost_myr"], "32.80")
        self.assertEqual(result["tolls_myr"], "10.00")
        self.assertEqual(result["total_known_cost_myr"], "42.80")
        self.assertEqual(result["per_person_known_cost_myr"], "10.70")
        self.assertTrue(result["tolls_included"])

    def test_one_way_and_omitted_tolls_are_explicit(self):
        result = calculate_trip_cost(
            distance_km=120,
            trip_type="one_way",
            fuel_consumption_l_per_100km=6.5,
            fuel_price_myr_per_l=2.05,
            tolls_myr=None,
            passengers=3,
        )
        self.assertEqual(result["distance_km"], "120.00")
        self.assertEqual(result["fuel_liters_estimate"], "7.800")
        self.assertEqual(result["fuel_cost_myr"], "15.99")
        self.assertIsNone(result["tolls_myr"])
        self.assertFalse(result["tolls_included"])
        self.assertIn("Fuel-only", result["note"])

    def test_zero_price_and_zero_tolls_are_valid(self):
        result = calculate_trip_cost(
            distance_km=10,
            trip_type="one_way",
            fuel_consumption_l_per_100km=5,
            fuel_price_myr_per_l=0,
            tolls_myr=0,
            passengers=1,
        )
        self.assertEqual(result["total_known_cost_myr"], "0.00")
        self.assertEqual(result["tolls_myr"], "0.00")

    def test_tolls_are_not_doubled_for_round_trip(self):
        result = calculate_trip_cost(
            distance_km=50,
            trip_type="round_trip",
            fuel_consumption_l_per_100km=10,
            fuel_price_myr_per_l=1,
            tolls_myr=3.25,
            passengers=1,
        )
        self.assertEqual(result["tolls_myr"], "3.25")

    def test_rejects_invalid_inputs(self):
        base = dict(
            distance_km=100,
            trip_type="one_way",
            fuel_consumption_l_per_100km=7,
            fuel_price_myr_per_l=2,
            tolls_myr=0,
            passengers=1,
        )
        for field, value in (
            ("distance_km", 0),
            ("distance_km", -1),
            ("distance_km", float("inf")),
            ("fuel_consumption_l_per_100km", 0),
            ("fuel_price_myr_per_l", -0.01),
            ("tolls_myr", -1),
            ("trip_type", "return"),
            ("passengers", 0),
            ("passengers", True),
            ("passengers", 1.5),
        ):
            bad = {**base, field: value}
            with self.subTest(field=field, value=value), self.assertRaises(InputError):
                calculate_trip_cost(**bad)

    def test_handler_returns_json_on_success_and_error(self):
        good = estimate_road_trip_cost(
            {
                "distance_km": 100,
                "trip_type": "round_trip",
                "fuel_consumption_l_per_100km": 8,
                "fuel_price_myr_per_l": 2.05,
                "tolls_myr": 10,
                "passengers": 4,
            }
        )
        self.assertTrue(json.loads(good)["ok"])
        bad = estimate_road_trip_cost({"distance_km": -1})
        self.assertFalse(json.loads(bad)["ok"])


if __name__ == "__main__":
    unittest.main()
