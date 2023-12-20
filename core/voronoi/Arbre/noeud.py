class Noeud:

    def __init__(self, data):
        self._data = data
        self._gauche = None
        self._droit = None
        self._parent = None
