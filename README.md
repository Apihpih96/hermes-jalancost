# JalanCost

JalanCost is a small, offline Hermes tool for estimating a road trip's fuel cost and splitting the known total among passengers. It uses only values the user supplies; it does not look up routes, traffic, fuel prices, or tolls.

## What it calculates

`estimate_road_trip_cost` takes one-way distance, one-way or round-trip mode, vehicle consumption in L/100 km, fuel price in MYR/L, passenger count, and optional total tolls for the selected journey. It returns estimated distance and litres, fuel cost, whether tolls were included, known total, and per-person share. If tolls are omitted, the result is explicitly fuel-only.

Example inputs: 100 km one way, round trip, 8 L/100 km, RM2.05/L, RM10.00 total tolls, 4 passengers. Expected output: 200.00 km, 16.000 L, RM32.80 fuel, RM10.00 tolls, RM42.80 known total, RM10.70 each. These are illustrative inputs, not current Malaysian prices or toll data.

## Privacy and behavior disclosures

- No network calls or third-party services.
- No reads outside the plugin's supplied tool inputs.
- No shell commands or child processes.
- No long-running background process.
- No credentials requested, read, or stored.
- No telemetry or usage reporting.
- No user data is persisted by this plugin.

## Installation and verification

The catalog listing will point at this repository's `jalancost/` subdirectory. On Hermes v0.22.7 or newer, validate that directory with:

```sh
hermes plugins validate ./jalancost --install-deps
hermes plugins doctor ./jalancost --ci
```

After review and catalog installation, enable `jalancost` and ask Hermes to estimate a trip using values you provide. The plugin itself does not fetch missing values.

The standalone tests are run from the repository root:

```sh
python -m unittest discover -s tests -v
```

## Compatibility and test status

The proposed compatibility floor is Hermes `>=0.22.7`, the version used for the recorded Linux validation and direct tool invocation. Six standalone unit tests pass. The recorded stable Linux validator run passed 15 checks. The direct test example returned RM42.80 total and RM10.70 per person.

These checks do not demonstrate an LLM/model-issued call, Android/Termux support, or catalog admission. The official Termux documentation currently says that the Termux package is broken; do not describe JalanCost as tested on Android.
