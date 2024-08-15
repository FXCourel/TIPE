from foronoi.graphe.point import Point
from foronoi.events.event import Event
from foronoi.observers.subject import Subject
from decimal import *


class SiteEvent(Event, Subject):
    circle_event = False

    def __init__(self, point: Point) -> None:
        """
        Un évènement de type site (site event).
        """
        super().__init__()
        self.point = point

    @property
    def xd(self) -> Decimal:
        return self.point.xd

    @property
    def yd(self) -> Decimal:
        return self.point.yd

    def __repr__(self) -> str:
        return f"SiteEvent(x={self.point.xd}, y={self.point.yd})"
