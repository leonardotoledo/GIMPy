from numpy import array

class Element:
    def __init__(self, nodes, left_neighbor=None, right_neighbor=None):
        self.__nodes = nodes
        self.__left_neighbor = left_neighbor
        self.__right_neighbor = right_neighbor

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return 'Element class'

    @property
    def nodes(self):
        return self.__nodes

    @property
    def left_neighbor(self):
        return self.__left_neighbor

    @property
    def right_neighbor(self):
        return self.__right_neighbor

    @nodes.setter
    def nodes(self, Nodes):
        self.__nodes = Nodes

    @left_neighbor.setter
    def left_neighbor(self, Elem):
        self.__left_neighbor = Elem

    @right_neighbor.setter
    def right_neighbor(self, Elem):
        self.__right_neighbor = Elem

    def reset(self):
        self.__nodes[0].reset()
        self.__nodes[1].reset()