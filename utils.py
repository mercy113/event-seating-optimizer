MAX_HALL_CAPACITY = 300
MAX_BALCONY_CAPACITY = 200
MAX_TOTAL_CAPACITY = 500


def normalize_section(value):
    value = str(value or "Any").strip().lower()

    if value == "hall":
        return "Hall"

    if value == "balcony":
        return "Balcony"

    return "Any"


def normalize_priority(value):
    value = str(value or "Standard").strip().lower()

    if value == "vip":
        return "VIP"

    return "Standard"


def normalize_venue(
    venue_type,
    hall_capacity=300,
    balcony_capacity=200
):
    venue_type = str(
        venue_type or "both"
    ).lower()

    try:
        hall_capacity = int(
            hall_capacity
        )
    except (TypeError, ValueError):
        hall_capacity = 300

    try:
        balcony_capacity = int(
            balcony_capacity
        )
    except (TypeError, ValueError):
        balcony_capacity = 200

    hall_capacity = max(
        0,
        min(
            hall_capacity,
            MAX_HALL_CAPACITY
        )
    )

    balcony_capacity = max(
        0,
        min(
            balcony_capacity,
            MAX_BALCONY_CAPACITY
        )
    )

    if venue_type == "hall":
        balcony_capacity = 0

    elif venue_type == "balcony":
        hall_capacity = 0

    return (
        hall_capacity,
        balcony_capacity
    )


def capacity_status(
    guest_count,
    hall_capacity,
    balcony_capacity
):
    total_capacity = (
        hall_capacity +
        balcony_capacity
    )

    if guest_count > total_capacity:
        return {
            "status": "OVER_CAPACITY",
            "label": "HOUSE FULL",
            "remaining": 0,
            "over_capacity":
                guest_count -
                total_capacity
        }

    if guest_count == total_capacity:
        return {
            "status": "FULL",
            "label": "HOUSE FULL",
            "remaining": 0,
            "over_capacity": 0
        }

    return {
        "status": "AVAILABLE",
        "label": "AVAILABLE",
        "remaining":
            total_capacity -
            guest_count,
        "over_capacity": 0
    }