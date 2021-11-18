from numpy import array, ceil
from node import Node
from element import Element
from grid import Grid
from particle import Particle

class Domain:
    def __init__(self, grid=None, particles=None, materials=None, b=0):

        if materials is None: materials = list()

        self.__grid = grid
        self.__particles = particles
        self.__materials = materials
        self.__b = b

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return 'Domain class'

    @property
    def grid(self):
        return self.__grid

    @property
    def particles(self):
        return self.__particles

    @property
    def b(self):
        return self.__b

    @property
    def materials(self):
        return self.__materials

    @grid.setter
    def grid(self, Grid):
        self.__grid = Grid

    @particles.setter
    def particles(self, Particles):
        self.__particles = Particles

    @b.setter
    def b(self, B):
        self.__b = B

    @materials.setter
    def materials(self, Materials):
        self.__materials = Materials

    def addMaterial(self, material):
        self.materials.append(material)

    def genGrid(self, dx, xmin, xmax):

        num_elem = (int) ( ceil(xmax-xmin)/dx )
        num_nodes = num_elem + 1

        nodes = array([Node(xmin+i*dx) for i in range(num_nodes)], dtype=Node)

        elements = array([Element([nodes[i], nodes[i+1]]) for i in range(num_elem)], dtype=Element)

        for i in range(num_elem):

            v1 = i-1
            v2 = i+1

            if v1 >= 0:
                elements[i].left_neighbor = elements[v1]

            if v2 < num_elem:
                elements[i].right_neighbor = elements[v2]

        self.grid = Grid(nodes, elements, dx, xmin, xmax)

    def genParticles(self, material, ppe, xmin, xmax):

        self.addMaterial(material)

        dxp = self.grid.L/ppe

        num_particles = (int) ( ceil(xmax-xmin)/dxp )

        mass = dxp*material.rho

        self.particles = array([Particle(xmin+(i+0.5)*dxp, mass, material, 0.5*dxp) for i in range(num_particles)], dtype=Particle)