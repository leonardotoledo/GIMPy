from numpy import array

class Element:
    def __init__(self, nodes):
        self.__nodes = nodes

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return 'Element class'

    @property
    def nodes(self):
        return self.__nodes

    @nodes.setter
    def nodes(self, Nodes):
        self.__nodes = Nodes

    def reset(self):
        self.__nodes[0].reset()
        self.__nodes[1].reset()
        self.__nodes[2].reset()
        self.__nodes[3].reset()