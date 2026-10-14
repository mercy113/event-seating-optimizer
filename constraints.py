def is_adjacent(
    section,
    guest_a,
    guest_b
):
    if (
        guest_a not in section
        or
        guest_b not in section
    ):
        return False

    index_a = section.index(
        guest_a
    )

    index_b = section.index(
        guest_b
    )

    return abs(
        index_a - index_b
    ) == 1


def together_ok(
    hall,
    balcony,
    together
):
    for guest_a, guest_b in together:

        same_hall = (
            guest_a in hall
            and
            guest_b in hall
        )

        same_balcony = (
            guest_a in balcony
            and
            guest_b in balcony
        )

        if not same_hall and not same_balcony:
            return False

        if same_hall:
            if not is_adjacent(
                hall,
                guest_a,
                guest_b
            ):
                return False

        if same_balcony:
            if not is_adjacent(
                balcony,
                guest_a,
                guest_b
            ):
                return False

    return True


def apart_ok(
    hall,
    balcony,
    apart
):
    for guest_a, guest_b in apart:

        if (
            guest_a in hall
            and
            guest_b in hall
            and
            is_adjacent(
                hall,
                guest_a,
                guest_b
            )
        ):
            return False

        if (
            guest_a in balcony
            and
            guest_b in balcony
            and
            is_adjacent(
                balcony,
                guest_a,
                guest_b
            )
        ):
            return False

    return True


def groups_ok(
    section_map,
    groups
):
    group_sections = {}

    for guest, group in groups.items():

        if guest not in section_map:
            continue

        section = section_map[guest]

        if group in group_sections:

            if (
                group_sections[group]
                != section
            ):
                return False

        else:
            group_sections[group] = section

    return True


def all_constraints_ok(
    hall,
    balcony,
    together,
    apart,
    groups,
    section_map
):
    return (
        groups_ok(
            section_map,
            groups
        )
        and
        together_ok(
            hall,
            balcony,
            together
        )
        and
        apart_ok(
            hall,
            balcony,
            apart
        )
    )