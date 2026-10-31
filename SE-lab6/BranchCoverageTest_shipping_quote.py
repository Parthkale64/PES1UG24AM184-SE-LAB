"""Exercise the cutoffs, early exits and resets in shipping decisions."""

import pytest

from shipping_quote import monitor_container_pressures, process_shipments


def test_fragile_hazmat_voids_only_its_own_shipment():
    shipments = [
        {
            "manifest_approved": True,
            "is_fragile": True,
            "packages": [
                {"weight_kg": 10},
                {"weight_kg": 2, "is_hazmat": True},
                {"weight_kg": 30},
            ],
        },
        {"manifest_approved": True, "packages": [{"weight_kg": 1}]},
    ]
    assert process_shipments(shipments, 5) == {
        "total_quote": 9.0, "status": "CLEARED"
    }


@pytest.mark.parametrize(("weight", "expected"), [(30, 360.0), (30.01, 540.18)])
def test_heavy_air_rate_applies_only_above_thirty_kg(weight, expected):
    shipment = {
        "manifest_approved": True,
        "mode": "air",
        "packages": [{"weight_kg": weight}],
    }
    assert process_shipments([shipment], 0) == {
        "total_quote": expected, "status": "CLEARED"
    }


@pytest.mark.parametrize(("count", "status"), [(3, "CLEARED"), (4, "FLAGGED_REVIEW")])
def test_review_threshold_counts_rejections_across_shipments(count, status):
    unsupported = {"manifest_approved": True, "mode": "sea"}
    shipments = [unsupported] * (count - 1) + [{
        "manifest_approved": True,
        "express_priority": True,
        "packages": [{"weight_kg": 0}, {"weight_kg": 2}],
    }]
    assert process_shipments(shipments, 0) == {
        "total_quote": 10.0, "status": status
    }


@pytest.mark.parametrize(("logs", "status"), [
    ([[13.9, 14.0, 13.9]], "STABLE"),
    ([[13.9], [], [13.9]], "STABLE"),
    ([[], [14.0, 13.9, 13.9]], "LEAK_DETECTED"),
])
def test_pressure_streak_requires_consecutive_lows_in_one_container(logs, status):
    assert monitor_container_pressures(logs) == status
