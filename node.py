class Node:
    def __init__(self, id, coord, mass=0.0, force=0.0, momentum=0.0, is_locked=False):
        self.__id = id
        self.__coord = coord
        self.__mass = mass
        self.__force = force
        self.__momentum = momentum
        self.__is_locked = is_locked

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return 'Node class'

    @property
    def id(self):
        return self.__id

    @property
    def coord(self):
        return self.__coord

    @property
    def mass(self):
        return self.__mass

    @property
    def force(self):
        return self.__force

    @property
    def momentum(self):
        return self.__momentum

    @property
    def is_locked(self):
        return self.__is_locked

    @id.setter
    def id(self, Id):
        self.__id = Id

    @coord.setter
    def coord(self, Coord):
        self.__coord = Coord

    @mass.setter
    def mass(self, Mass):
        self.__mass = Mass

    @force.setter
    def force(self, Force):
        self.__force = Force

    @momentum.setter
    def momentum(self, Momentum):
        self.__momentum = Momentum

    def lock(self):
        self.__is_locked = True

    def unlock(self):
        self.__is_locked = False

    def reset(self):
        self.__mass = 0
        self.__force = 0.0
        self.__momentum = 0.0

    def N(self, px, lp, L):
        x = px - self.coord

        S = 0
        if ((-L - lp < x) and (x <= -L + lp)):
            S = (L + lp + x) * (L + lp + x) / (4 * L * lp)	
        else:
            if ((-L + lp < x) and (x <= -lp)):
                S = 1 + x / L	
            else:
                if ((-lp < x) and (x <= lp)):
                    S = 1 - (x * x + lp * lp) / (2 * L * lp)		
                else:
                    if ((lp < x) and (x <= L - lp)):
                        S = 1 - x / L			
                    else:
                        if ((L - lp < x) and (x <= L + lp)):
                            S = (L + lp - x) * (L + lp - x) / (4 * L * lp)

        return S

    def dN(self, px, lp, L):
        x = px - self.coord

        S = 0
        if ((-L - lp < x) and (x <= -L + lp)):
            S = (L + lp + x) / (2 * L * lp)
        else:
            if ((-L + lp < x) and (x <= -lp)):
                S = 1 / L	
            else:
                if ((-lp < x) and (x <= lp)):
                    S = -x / (L * lp)	
                else:
                    if ((lp < x) and (x <= L - lp)):
                        S = -1 / L			
                    else:
                        if ((L - lp < x) and (x <= L + lp)):
                            S = -(L + lp - x) / (2 * L * lp)

        return S