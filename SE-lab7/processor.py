"""Validate shipment inputs and display the resulting weights and labels."""

import json
import math
import re


def calculate_dimensional_weight(dimensions_str):
    """Return dimensional weight in kg, or None for invalid dimensions."""
    if not isinstance(dimensions_str, str):
        return None
    parts = dimensions_str.split("x")
    if len(parts) != 3:
        return None
    try:
        dimensions = [float(part) for part in parts]
    except ValueError:
        return None
    if not all(math.isfinite(value) and value > 0 for value in dimensions):
        return None
    weight = math.prod(dimensions) / 5000
    return round(weight, 2) if math.isfinite(weight) else None


def format_tracking_label(raw_code):
    """Normalize a letter and digit sequence, or return None for invalid codes."""
    if not isinstance(raw_code, str) or not re.fullmatch(r"[A-Za-z][0-9]+", raw_code):
        return None
    digits = raw_code[1:].lstrip("0").zfill(6)
    return f"{raw_code[0].upper()}-{digits}"


def parse_package_manifest(json_payload):
    """Read a finite, nonnegative weight from a JSON object, or return None."""
    if not isinstance(json_payload, (str, bytes, bytearray)):
        return None
    try:
        data = json.loads(json_payload)
    except (ValueError, RecursionError):
        return None
    if not isinstance(data, dict):
        return None
    value = data.get("weight")
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        return None
    try:
        weight = float(value)
    except (ValueError, OverflowError):
        return None
    return weight if math.isfinite(weight) and weight >= 0 else None


def main():
    """Read and validate one set of shipping inputs."""
    print("==== Running calculate_dimensional_weight ====")
    dims_input = input("Enter dimensions LxWxH in cm (e.g. 20x30x10): ")
    dim_weight = calculate_dimensional_weight(dims_input)
    if dim_weight is None:
        print("Invalid dimensions. Enter three positive lengths in cm.")
    else:
        print("Dimensional Weight (kg):", dim_weight)

    print("\n==== Running format_tracking_label ====")
    code_input = input("Enter raw code (e.g. E123): ")
    label = format_tracking_label(code_input)
    if label is None:
        print("Invalid tracking code. Enter one letter followed by digits.")
    else:
        print("Formatted Label:", label)

    print("\n==== Running parse_package_manifest ====")
    json_input = input('Enter manifest JSON (e.g. {"weight": 12.5}): ')
    weight = parse_package_manifest(json_input)
    if weight is None:
        print("Invalid manifest. Supply a finite, nonnegative weight.")
    else:
        print("Manifest Weight:", weight)


if __name__ == "__main__":
    main()
