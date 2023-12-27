class Edge:

    def __init__(self) -> None:
        pass

    @property
    def twin(self):
        return self._twin

    @twin.setter
    def twin(self, twin):
        self._twin = twin
        if twin is not None:
            twin._twin = self

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next
        if next is not None:
            next._prev = self

    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, prev):
        self._prev = prev
        if prev is not None:
            prev._next = self