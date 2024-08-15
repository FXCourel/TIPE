from decimal import Decimal

from foronoi.graphe.coordonee import Coordonee


class Arc:
    def __init__(self, origine: Coordonee, circle_event=None):

        self.origine = origine
        self.circle_event = circle_event

    def __repr__(self):
        return f"Arc({self.origine.nom})"

    def get_plot(self, x, sweep_line):
        """
        Calcul les ordonées de la parabole pour des x donnés.
        """
        sweep_line = float(sweep_line)
        i = self.origine

        if i.y - sweep_line == 0:
            return None

        u = 2 * (i.y - sweep_line)
        v = (x ** 2 - 2 * i.x * x + i.x ** 2 + i.y ** 2 - sweep_line ** 2)
        y = v/u

        return y
