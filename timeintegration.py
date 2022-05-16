from numpy import array, max, sqrt

class TimeIntegration:
    def __init__(self, domain, tf, t0=0.0, t=0.0, dt=0, pct=0.1):
        self.__domain = domain
        self.__tf = tf
        self.__t0 = t0
        self.__t = t
        self.__dt = dt
        self.__pct = pct

        if dt == 0: self.computeDt()

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return 'Time integration class'

    @property
    def domain(self):
        return self.__domain

    @property
    def tf(self):
        return self.__tf

    @property
    def t(self):
        return self.__t

    @property
    def dt(self):
        return self.__dt

    @property
    def pct(self):
        return self.__pct

    @tf.setter
    def tf(self, Tf):
        self.__tf = Tf

    @t.setter
    def t(self, T):
        self.__t = T

    @dt.setter
    def dt(self, Dt):
        self.__dt = Dt

    def computeDt(self):
        
        c = max([sqrt(mat.E/mat.rho) for mat in self.domain.materials])

        dtc = self.domain.grid.L/c

        self.dt = self.pct*dtc

    def advance(self):

        # 1. Particle-To-Grid Mapping (P2G)
        self.domain.grid.reset()

        b = self.domain.b
        dx = self.domain.grid.L

        for p in self.domain.particles:
            e = self.domain.grid.mapParticle2Element(p)

            x = p.coord
            lp = p.lp

            for n in e.nodes:
                if not n.is_locked:
                    N = n.N(x, lp, dx)
                    dN = n.dN(x, lp, dx)

                    n.mass += p.mass * N
                    n.momentum += (p.mass * p.vel) * N

                    # External force
                    n.force += p.mass * b * N

                    # Internal force
                    n.force -= p.stress * p.vol * dN

        # 2. Update of nodal momentum
        for n in self.domain.grid.nodes:
            n.momentum += self.dt*n.force

        # 3. Grid-To-Particle (G2P)
        for p in self.domain.particles:
            e = self.domain.grid.mapParticle2Element(p)

            x = p.coord
            lp = p.lp

            for n in e.nodes:
                if not n.is_locked and n.mass > 0:
                    N = n.N(x, lp, dx)

                    p.vel += self.dt * n.force/n.mass * N
                    p.coord += self.dt * n.momentum/n.mass * N

        # 4. Computation of particles stresses
        for p in self.domain.particles:
            e = self.domain.grid.mapParticle2Element(p)

            x = p.coord
            lp = p.lp

            Lp = 0
            for n in e.nodes:
                if not n.is_locked and n.mass > 0:
                    dN = n.dN(x, lp, dx)
                    
                    Lp += n.momentum/n.mass*dN

            p.def_gradient *= 1 + self.dt*Lp

            p.vol = p.def_gradient*p.init_vol

            dE = self.dt*Lp

            p.strain += dE

            p.stress += p.mat.E*dE

        self.t += self.dt