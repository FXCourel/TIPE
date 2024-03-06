from Graphe.point import Point

class Polygone:
    
    def __init__(self, coordinates: list[tuple[float, float]]):
        self.points = [Point(x, y) for x, y in coordinates]
        