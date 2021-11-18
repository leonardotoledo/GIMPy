class Material:
    def __init__(self, E, rho, nu):
        self.__E = E
        self.__rho = rho
        self.__nu = nu

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return 'Material class'

    @property
    def E(self):
        return self.__E

    @property
    def rho(self):
        return self.__rho

    @property
    def nu(self):
        return self.__nu