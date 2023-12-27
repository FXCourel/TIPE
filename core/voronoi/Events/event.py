SITE_EVENT = 0
CIRCLE_EVENT = 1


class Event:

    def __init__(self, data, type, arc=None) -> None:
        self._type = type
        if self.is_site_event():
            self._site = data
            self._prio = self._site[1]
        elif self.is_circle_event() and arc is not None:
            self._circle = data
            self._prio = self._circle[1]
            self._leaf = arc
        else:
            raise TypeError('Event ni de type site-event ni circle-event')

    def __str__(self) -> str:
        return f"Event({self._type})"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def type(self):
        return self._type
    
    @property
    def site(self):
        if self.is_site_event():
            return self._site
        else:
            raise TypeError('Event n\'est pas un site-event')
        
    @property
    def circle(self):
        if self.is_circle_event():
            return self._circle
        else:
            raise TypeError('Event n\'est pas un circle-event')
       
    @property
    def leaf(self):
        if self.is_circle_event():
            return self._leaf
        else:
            raise TypeError('Event n\'est pas un circle-event')
        
    def __gt__(self, other):
        return self._prio > other._prio

    def is_site_event(self) -> bool:
        return self.type == SITE_EVENT

    def is_circle_event(self) -> bool:
        return self.type == CIRCLE_EVENT