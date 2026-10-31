"""Check the prices, statuses and pressure readings returned by the ledger."""

import pytest

from shipping_quote import monitor_container_pressures, process_shipments


def test_single_ground_shipment():
    shipment = {
        "manifest_approved": True,
        "mode": "ground",
        "packages": [{"weight_kg": 10}],
    }
    assert process_shipments([shipment], 20) == {
        "total_quote": 60.0, "status": "CLEARED"
    }


@pytest.mark.parametrize(("shipments", "fee"), [(None, 0), ([], -1)])
def test_invalid_inputs(shipments, fee):
    with pytest.raises(ValueError, match="Invalid shipments list or handling fee"):
        process_shipments(shipments, fee)


def test_express_air_with_heavy_and_hazardous_packages():
    shipment = {
        "manifest_approved": True,
        "mode": "air",
        "express_priority": True,
        "packages": [{"weight_kg": 40}, {"weight_kg": 2, "is_hazmat": True}],
    }
    # (10 handling + 40 * 18 heavy air rate + 50 hazmat fee) * 1.25
    assert process_shipments([shipment], 10) == {
        "total_quote": 975.0, "status": "CLEARED"
    }


def test_four_rejections_require_review():
    shipments = [
        {"manifest_approved": True, "mode": "sea"},
        {"manifest_approved": True, "packages": [{}, {"weight_kg": -1}, {}]},
    ]
    assert process_shipments(shipments, 0) == {
        "total_quote": 0.0, "status": "FLAGGED_REVIEW"
    }


def test_unapproved_manifest_has_no_cargo_or_handling_fee():
    assert process_shipments([{"packages": [{"weight_kg": 10}]}], 20) == {
        "total_quote": 0.0, "status": "NO_CARGO"
    }


@pytest.mark.parametrize(("logs", "status"), [
    ([], "NO_DATA"),
    ([[14.0, 15.0]], "STABLE"),
    ([[13.0, 13.9]], "LEAK_DETECTED"),
])
def test_pressure_status(logs, status):
    assert monitor_container_pressures(logs) == status
