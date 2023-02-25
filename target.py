from dataclasses import dataclass


@dataclass()
class Target:
    id: int
    probability: float
