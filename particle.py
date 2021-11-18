class Particle:
    def __init__(self, coord, mass, mat, lp, vel=0.0, stress=0.0, strain=0.0, def_gradient=1.0):
        self.__coord = coord
        self.__mass = mass
        self.__mat = mat
        self.__lp = lp
        self.__init_vol = 2.0*lp
        self.__vol = 2.0*lp
        self.__vel = vel
        self.__stress = stress
        self.__strain = strain
        self.__def_gradient = def_gradient

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return 'Particle class'

    @property
    def coord(self):
        return self.__coord

    @property
    def mass(self):
        return self.__mass

    @property
    def mat(self):
        return self.__mat

    @property
    def lp(self):
        return self.__lp

    @property
    def init_vol(self):
        return self.__init_vol

    @property
    def vol(self):
        return self.__vol

    @property
    def vel(self):
        return self.__vel

    @property
    def stress(self):
        return self.__stress

    @property
    def strain(self):
        return self.__strain

    @property
    def def_gradient(self):
        return self.__def_gradient

    @coord.setter
    def coord(self, Coord):
        self.__coord = Coord

    @mass.setter
    def mass(self, Mass):
        self.__mass = Mass

    @mat.setter
    def mat(self, Mat):
        self.__mat = Mat

    @lp.setter
    def lp(self, Lp):
        self.__lp = Lp

    @init_vol.setter
    def init_vol(self, Vol):
        self.__init_vol = Vol

    @vol.setter
    def vol(self, Vol):
        self.__vol = Vol

    @vel.setter
    def vel(self, Vel):
        self.__vel = Vel

    @stress.setter
    def stress(self, Stress):
        self.__stress = Stress

    @strain.setter
    def strain(self, Strain):
        self.__strain = Strain

    @def_gradient.setter
    def def_gradient(self, F):
        self.__def_gradient = F