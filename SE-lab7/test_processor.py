"""Property tests for shipment dimensions, tracking labels and manifest weights."""

import json
import math
import re
import string

from hypothesis import example, given, strategies as st

from processor import (
    calculate_dimensional_weight,
    format_tracking_label,
    parse_package_manifest,
)


@given(st.text(max_size=80) | st.none() | st.integers())
@example("-2x30x10")
@example("1x2x3x4")
@example("1x2xinf")
def test_dimension_input_has_a_finite_weight_or_is_rejected(value):
    result = calculate_dimensional_weight(value)
    parts = value.split("x") if isinstance(value, str) else []
    try:
        numbers = [float(part) for part in parts]
    except ValueError:
        numbers = []
    if len(numbers) != 3 or not all(math.isfinite(n) and n > 0 for n in numbers):
        assert result is None
    else:
        volume_weight = math.prod(numbers) / 5000
        expected = round(volume_weight, 2) if math.isfinite(volume_weight) else None
        assert result == expected


@given(st.integers(1, 500), st.integers(1, 500), st.integers(1, 500))
def test_dimensions_follow_the_volume_formula(length, width, height):
    result = calculate_dimensional_weight(f"{length}x{width}x{height}")
    assert result == round(length * width * height / 5000, 2)


@given(st.text(max_size=80) | st.none() | st.integers())
@example("1123")
@example("E-12")
def test_tracking_label_accepts_one_letter_then_decimal_digits(value):
    result = format_tracking_label(value)
    if isinstance(value, str) and re.fullmatch(r"[a-zA-Z][0-9]+", value):
        assert result == f"{value[0].upper()}-{int(value[1:]):06d}"
    else:
        assert result is None


@given(st.sampled_from(string.ascii_letters), st.integers(0, 10**9), st.integers(0, 4))
def test_tracking_numbers_keep_their_value(letter, number, leading_zeros):
    code = letter + "0" * leading_zeros + str(number)
    assert format_tracking_label(code) == f"{letter.upper()}-{number:06d}"


@given(st.text(max_size=80) | st.none() | st.integers())
@example('{"weight": -1}')
@example('{"weight": true}')
@example('{"weight": "NaN"}')
def test_manifest_returns_only_finite_nonnegative_weights(payload):
    result = parse_package_manifest(payload)
    if result is not None:
        data = json.loads(payload)
        assert isinstance(data, dict)
        assert not isinstance(data["weight"], bool)
        assert result == float(data["weight"])
        assert math.isfinite(result) and result >= 0


@given(st.integers(0, 100000), st.booleans())
def test_manifest_reads_numeric_and_text_weights(grams, use_text):
    weight = grams / 1000
    payload = json.dumps({"weight": str(weight) if use_text else weight})
    assert parse_package_manifest(payload) == weight
