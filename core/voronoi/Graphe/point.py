from decimal import Decimal


class Point:

    def __init__(self, x, y) -> None:
        self._x: Decimal = Point._to_dec(x)
        self._y: Decimal = Point._to_dec(y)

    def __add__(self, other):
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return Point(x=self.x - other.x, y=self.y - other.y)

    def __repr__(self) -> str:
        return f"Point({self.x:.2f}, {self.y:.2f})"

    @property
    def x(self):
        return float(self._x)

    @x.setter
    def x(self, value):
        self._x = Point._to_dec(value)

    @property
    def y(self):
        return float(self._y)

    @y.setter
    def y(self, value):
        self._y = Point._to_dec(value)

    @property
    def x_decimal(self):
        return self._x

    @property
    def y_decimal(self):
        return self._y

    @property
    def coordinates(self):
        return self.x, self.y

    @coordinates.setter
    def coordinates(self, value: tuple):
        self.x, self.y = (Point._to_dec(v) for v in value)

    @property
    def coordinates_decimal(self):
        return self.x_decimal, self.y_decimal

    @staticmethod
    def _to_dec(value):
        return Decimal(str(value)) if value is not None else None
