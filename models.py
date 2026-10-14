from dataclasses import dataclass


@dataclass
class Guest:
    name: str
    group: str = "General"
    priority: str = "Standard"
    preferred_section: str = "Any"