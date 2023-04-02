from dataclasses import dataclass


@dataclass()
class Params:
    mu: list
    lambda0: float
    systems_count: int
    batch: list
    links: list
