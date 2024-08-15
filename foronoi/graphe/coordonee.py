from decimal import Decimal


class Coordonee:
    def __init__(self, x=None, y=None) -> None:
        """
        Un point du plan
        """
        self._xd: Decimal = Coordonee._to_dec(x)
        self._yd: Decimal = Coordonee._to_dec(y)

    def __sub__(self, other) -> "Coordonee":
        return Coordonee(x=self.xd - other.xd, y=self.yd - other.yd)

    def __repr__(self) -> str:
        return f"Coord({self.xd:.2f}, {self.yd:.2f})"

    @staticmethod
    def _to_dec(value) -> Decimal:
        return Decimal(str(value)) if value is not None else None

    @property
    def x(self) -> float:
        return float(self._xd)

    @property
    def y(self) -> float:
        return float(self._yd)

    @x.setter
    def x(self, value) -> None:
        self._xd = Coordonee._to_dec(value)

    @y.setter
    def y(self, value) -> None:
        self._yd = Coordonee._to_dec(value)

    @property
    def xy(self) -> tuple[float, float]:
        return self.x, self.y

    @property
    def xd(self):
        return self._xd

    @xd.setter
    def xd(self, value: float):
        self._xd = Coordonee._to_dec(value)

    @property
    def yd(self):
        return self._yd

    @yd.setter
    def yd(self, value: float):
        self._yd = Coordonee._to_dec(value)
