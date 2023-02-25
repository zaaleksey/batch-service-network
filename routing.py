from collections import defaultdict

from target import Target


class Routing:

    def __init__(self, links: list[tuple]) -> None:
        self.map = defaultdict(list)
        [self.map[link[0]].append(Target(link[1], link[2])) for link in links]
