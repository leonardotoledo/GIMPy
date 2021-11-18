from numpy import ceil


class Grid:
    def __init__(self, nodes, elements, L, xmin, xmax):
        self.__nodes = nodes
        self.__elements = elements
        self.__L = L
        self.__xmin = xmin
        self.__xmax = xmax

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return 'Grid class'

    @property
    def nodes(self):
        return self.__nodes

    @property
    def elements(self):
        return self.__elements

    @property
    def L(self):
        return self.__L

    @property
    def xmin(self):
        return self.__xmin

    @property
    def xmax(self):
        return self.__xmax

    def reset(self):
        for e in self.elements: e.reset()

    def lockNodeAtCoord(self, coord):
        for e in self.elements:
            for n in e.nodes:
                if n.coord == coord:
                    n.lock()
                    return

    def mapParticle2Element(self, particle):
        id = (int) ( ceil((particle.coord - self.xmin)/self.L) )

        if id < 1 or id > len(self.elements):
            raise ValueError('A particle has gone outside the grid domain limits.')

        return self.elements[id-1]