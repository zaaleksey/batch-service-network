from collections import defaultdict
from dataclasses import dataclass


class Routing:

    def __init__(self, links: list[tuple]) -> None:
        self.map = defaultdict(list)
        [self.map[link[0]].append(Target(link[1], link[2])) for link in links]


@dataclass()
class Target:
    id: int
    probability: float


def get_links_by_theta(theta: list[list]) -> list:
    links = []
    for i in range(len(theta)):
        for j in range(len(theta[i])):
            if theta[i][j] != 0:
                links.append((i, j, theta[i][j]))
    return links
