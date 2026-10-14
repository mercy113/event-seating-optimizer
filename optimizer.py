import time

from constraints import (
    all_constraints_ok
)


class SeatingOptimizer:

    def __init__(
        self,
        guests,
        together=None,
        apart=None,
        hall_capacity=300,
        balcony_capacity=200
    ):

        self.guests = guests

        self.together = (
            together or []
        )

        self.apart = (
            apart or []
        )

        self.hall_capacity = (
            hall_capacity
        )

        self.balcony_capacity = (
            balcony_capacity
        )

        self.nodes = 0
        self.backtracks = 0

    # -------------------------------------------------
    # Build connected components
    # -------------------------------------------------

    def _build_components(
        self,
        guests,
        together
    ):

        names = [
            guest.name
            for guest in guests
        ]

        parent = {
            name: name
            for name in names
        }

        def find(name):

            while parent[name] != name:

                parent[name] = parent[
                    parent[name]
                ]

                name = parent[name]

            return name

        def union(
            first,
            second
        ):

            root_a = find(first)
            root_b = find(second)

            if root_a != root_b:
                parent[root_b] = root_a

        # Together connections
        for first, second in together:

            if (
                first in parent
                and
                second in parent
            ):
                union(
                    first,
                    second
                )

        # Same group connections
        groups = {}

        for guest in guests:

            groups.setdefault(
                guest.group,
                []
            ).append(
                guest.name
            )

        for group_names in groups.values():

            if len(group_names) > 1:

                first = group_names[0]

                for name in group_names[1:]:

                    union(
                        first,
                        name
                    )

        components = {}

        for guest in guests:

            root = find(
                guest.name
            )

            components.setdefault(
                root,
                []
            ).append(
                guest
            )

        return list(
            components.values()
        )

    # -------------------------------------------------
    # Determine preferred section
    # -------------------------------------------------

    def _preferred_section(
        self,
        block
    ):

        sections = {
            guest.preferred_section
            for guest in block
        }

        if (
            "Hall" in sections
            and
            "Balcony" in sections
        ):
            return "Either"

        if "Hall" in sections:
            return "Hall"

        if "Balcony" in sections:
            return "Balcony"

        return "Any"

    # -------------------------------------------------
    # Order guests inside a block
    # -------------------------------------------------

    def _order_block(
        self,
        block,
        together
    ):

        names = {
            guest.name
            for guest in block
        }

        adjacency = {
            name: []
            for name in names
        }

        for first, second in together:

            if (
                first in names
                and
                second in names
            ):

                adjacency[first].append(
                    second
                )

                adjacency[second].append(
                    first
                )

        # No together relation
        if not any(adjacency.values()):

            return block

        ordered_names = []
        remaining = set(names)

        # Start with an endpoint if possible
        start = None

        for name in names:

            if len(adjacency[name]) <= 1:
                start = name
                break

        if start is None:
            start = next(
                iter(names)
            )

        current = start
        previous = None

        while current is not None:

            if current in remaining:

                ordered_names.append(
                    current
                )

                remaining.remove(
                    current
                )

            next_guest = None

            for neighbor in adjacency[current]:

                if (
                    neighbor != previous
                    and
                    neighbor in remaining
                ):

                    next_guest = neighbor
                    break

            previous = current
            current = next_guest

        # Add any disconnected names
        ordered_names.extend(
            sorted(
                remaining
            )
        )

        guest_map = {
            guest.name: guest
            for guest in block
        }

        return [
            guest_map[name]
            for name in ordered_names
        ]

    # -------------------------------------------------
    # Solve
    # -------------------------------------------------

    def solve(self):

        start_time = time.perf_counter()

        total_guests = len(
            self.guests
        )

        total_capacity = (
            self.hall_capacity +
            self.balcony_capacity
        )

        if (
            total_guests
            >
            total_capacity
        ):
            return None

        if total_guests == 0:
            return None

        valid_names = {
            guest.name
            for guest in self.guests
        }

        together = [
            pair
            for pair in self.together
            if (
                len(pair) == 2
                and
                pair[0] in valid_names
                and
                pair[1] in valid_names
            )
        ]

        apart = [
            pair
            for pair in self.apart
            if (
                len(pair) == 2
                and
                pair[0] in valid_names
                and
                pair[1] in valid_names
            )
        ]

        groups = {
            guest.name:
                guest.group
            for guest in self.guests
        }

        # Create blocks
        blocks = self._build_components(
            self.guests,
            together
        )

        # Order larger/VIP/preferred blocks first
        def block_score(block):

            vip_count = sum(
                guest.priority.upper()
                == "VIP"
                for guest in block
            )

            preferred_count = sum(
                guest.preferred_section
                != "Any"
                for guest in block
            )

            return (
                len(block),
                vip_count,
                preferred_count
            )

        blocks.sort(
            key=block_score,
            reverse=True
        )

        # Check impossible block
        for block in blocks:

            if len(block) > max(
                self.hall_capacity,
                self.balcony_capacity
            ):
                return None

        assignment = {}

        hall_blocks = []
        balcony_blocks = []

        # ---------------------------------------------
        # Search
        # ---------------------------------------------

        def build_section_map():

            mapping = {}

            for index, section in assignment.items():

                block = blocks[index]

                for guest in block:

                    mapping[
                        guest.name
                    ] = section

            return mapping

        def current_names(
            block_list
        ):

            result = []

            for block_index in block_list:

                block = blocks[
                    block_index
                ]

                ordered = self._order_block(
                    block,
                    together
                )

                result.extend(
                    guest.name
                    for guest in ordered
                )

            return result

        def search(
            block_index,
            hall_used,
            balcony_used
        ):

            self.nodes += 1

            if block_index == len(blocks):

                hall_names = current_names(
                    hall_blocks
                )

                balcony_names = current_names(
                    balcony_blocks
                )

                section_map = (
                    build_section_map()
                )

                if all_constraints_ok(
                    hall_names,
                    balcony_names,
                    together,
                    apart,
                    groups,
                    section_map
                ):
                    return True

                self.backtracks += 1

                return False

            block = blocks[
                block_index
            ]

            block_size = len(block)

            preference = (
                self._preferred_section(
                    block
                )
            )

            if preference == "Hall":

                options = [
                    "Hall",
                    "Balcony"
                ]

            elif preference == "Balcony":

                options = [
                    "Balcony",
                    "Hall"
                ]

            else:

                options = [
                    "Hall",
                    "Balcony"
                ]

            for section in options:

                if section == "Hall":

                    if (
                        hall_used +
                        block_size
                        >
                        self.hall_capacity
                    ):
                        continue

                    hall_blocks.append(
                        block_index
                    )

                    assignment[
                        block_index
                    ] = "Hall"

                    if search(
                        block_index + 1,
                        hall_used + block_size,
                        balcony_used
                    ):
                        return True

                    hall_blocks.pop()

                    assignment.pop(
                        block_index,
                        None
                    )

                else:

                    if (
                        balcony_used +
                        block_size
                        >
                        self.balcony_capacity
                    ):
                        continue

                    balcony_blocks.append(
                        block_index
                    )

                    assignment[
                        block_index
                    ] = "Balcony"

                    if search(
                        block_index + 1,
                        hall_used,
                        balcony_used + block_size
                    ):
                        return True

                    balcony_blocks.pop()

                    assignment.pop(
                        block_index,
                        None
                    )

            self.backtracks += 1

            return False

        solved = search(
            0,
            0,
            0
        )

        if not solved:
            return None

        hall = current_names(
            hall_blocks
        )

        balcony = current_names(
            balcony_blocks
        )

        section_map = {}

        for name in hall:
            section_map[name] = "Hall"

        for name in balcony:
            section_map[name] = "Balcony"

        # Final validation
        if not all_constraints_ok(
            hall,
            balcony,
            together,
            apart,
            groups,
            section_map
        ):
            return None

        elapsed = (
            time.perf_counter()
            -
            start_time
        ) * 1000

        efficiency = (
            total_guests /
            max(
                self.nodes,
                1
            )
        ) * 100

        return {

            "hall": hall,

            "balcony": balcony,

            "normal": hall,

            "normal_count":
                len(hall),

            "balcony_count":
                len(balcony),

            "hall_capacity":
                self.hall_capacity,

            "normal_capacity":
                self.hall_capacity,

            "balcony_capacity":
                self.balcony_capacity,

            "total_guests":
                total_guests,

            "total_capacity":
                total_capacity,

            "remaining_seats":
                total_capacity -
                total_guests,

            "nodes":
                self.nodes,

            "backtracks":
                self.backtracks,

            "elapsed_ms":
                round(
                    elapsed,
                    3
                ),

            "efficiency":
                round(
                    efficiency,
                    2
                )
        }