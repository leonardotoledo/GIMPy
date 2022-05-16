class Material:
    def __init__(self, E, rho):
        self.__E = E
        self.__rho = rho

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