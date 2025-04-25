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

        c = max([sqrt(mat.E / mat.rho) for mat in self.domain.materials])

        dtc = self.domain.grid.L / c

        self.dt = self.pct * dtc

    def initializeParticles(self):
        for p in self.domain.particles:
            p.element = self.domain.grid.mapParticle2Element(p)

    def usf(self):
        b = self.domain.b
        dx = self.domain.grid.L

        # 0. Reset nodal values
        for n in self.domain.grid.nodes:
            n.mass = 0
            n.momentum = 0
            n.force = 0

        # 1. Particle-To-Grid Mapping (P2G)
        for p in self.domain.particles:
            x = p.coord
            lp = p.lp

            for n in p.element.nodes:
                if not n.is_locked:
                    N = n.N(x, lp, dx)
                    n.mass += p.mass * N
                    n.momentum += (p.mass * p.vel) * N

        # 2. Grid-To-Particle (G2P)
        for p in self.domain.particles:
            x = p.coord
            lp = p.lp

            Lp = 0
            for n in p.element.nodes:
                if not n.is_locked and n.mass > 0:
                    dN = n.dN(x, lp, dx)
                    Lp += dN * n.momentum / n.mass

            p.def_gradient *= (1 + Lp * self.dt)
            p.vol = p.def_gradient * p.init_vol
            dE = self.dt * Lp
            p.strain += dE
            p.stress += p.mat.E * dE

            for n in p.element.nodes:
                if not n.is_locked and n.mass > 0:
                    dN = n.dN(x, lp, dx)
                    n.force -= dN * p.vol * p.stress

        # 3. Update nodal momentum
        for n in self.domain.grid.nodes:
            if not n.is_locked and n.mass > 0:
                n.momentum += self.dt * n.force

        # 4. Update particle kinematics
        for p in self.domain.particles:
            x = p.coord
            lp = p.lp

            for n in p.element.nodes:
                if not n.is_locked and n.mass > 0:
                    N = n.N(x, lp, dx)
                    p.vel += self.dt * N * n.force / n.mass
                    p.coord += self.dt * N * n.momentum / n.mass

            p.element = self.domain.grid.mapParticle2Element(p)

        self.t += self.dt

    def usl(self):
        b = self.domain.b
        dx = self.domain.grid.L

        # 0. Reset nodal values
        for n in self.domain.grid.nodes:
            n.mass = 0
            n.momentum = 0
            n.force = 0

        # 1. Particle-To-Grid Mapping (P2G)

        count = 0
        for p in self.domain.particles:
            x = p.coord
            lp = p.lp

            for n in p.element.nodes:
                N = n.N(x, lp, dx)
                dN = n.dN(x, lp, dx)
                nodalMassInc = p.mass * N
                nodalMomentumInc = (p.mass * p.vel) * N
                nodalForceInc = -dN * p.vol * p.stress

                # if n.id == 5 and p.id == 7:
                #     print(f'Node ID: {n.id}')

                n.mass += nodalMassInc
                n.momentum += nodalMomentumInc
                n.force += nodalForceInc

        # 2. Update nodal momentum
        for n in self.domain.grid.nodes:
            if n.mass > 0:
                n.momentum += self.dt * n.force
            if n.is_locked:
                n.mass = 0
                n.momentum = 0
                n.force = 0

        # 3. Grid-To-Particle (G2P)
        for p in self.domain.particles:
            x = p.coord
            lp = p.lp

            p.vel_gradient = 0
            count = 0
            for n in p.element.nodes:
                if not n.is_locked and n.mass > 0:
                    N = n.N(x, lp, dx)
                    dN = n.dN(x, lp, dx)
                    p.vel_gradient += dN * n.momentum / n.mass
                    p.vel += self.dt * N * n.force / n.mass
                    p.coord += self.dt * N * n.momentum / n.mass
                    count += 1

            p.def_gradient *= (1 + p.vel_gradient * self.dt)
            p.vol = p.def_gradient * p.init_vol
            dE = self.dt * p.vel_gradient
            p.strain += dE
            p.stress += p.mat.E * dE

            p.element = self.domain.grid.mapParticle2Element(p)

        self.t += self.dt

    def musl(self):
        b = self.domain.b
        dx = self.domain.grid.L

        # 0. Reset nodal values
        for n in self.domain.grid.nodes:
            n.mass = 0
            n.momentum = 0
            n.force = 0

        # 1. Particle-To-Grid Mapping (P2G)
        for p in self.domain.particles:
            x = p.coord
            lp = p.lp

            for n in p.element.nodes:
                if not n.is_locked:
                    N = n.N(x, lp, dx)
                    dN = n.dN(x, lp, dx)
                    n.mass += p.mass * N
                    n.momentum += (p.mass * p.vel) * N
                    n.force -= dN * p.vol * p.stress

        # 2. Update nodal momentum
        for n in self.domain.grid.nodes:
            if not n.is_locked and n.mass > 0:
                n.momentum += self.dt * n.force

        # 3. Grid-To-Particle (Update particle kinematics)
        for p in self.domain.particles:
            x = p.coord
            lp = p.lp

            for n in p.element.nodes:
                if not n.is_locked and n.mass > 0:
                    N = n.N(x, lp, dx)
                    p.vel += self.dt * N * n.force / n.mass
                    p.coord += self.dt * N * n.momentum / n.mass

            p.element = self.domain.grid.mapParticle2Element(p)

        # 4. Recalculate nodal momentum
        for n in self.domain.grid.nodes:
            n.mass = 0
            n.momentum = 0

        for p in self.domain.particles:
            x = p.coord
            lp = p.lp

            for n in p.element.nodes:
                if not n.is_locked:
                    N = n.N(x, lp, dx)
                    n.mass += p.mass * N
                    n.momentum += (p.mass * p.vel) * N

        # 5. Grid-To-Particle (Update particle stress)
        for p in self.domain.particles:
            x = p.coord
            lp = p.lp

            Lp = 0
            for n in p.element.nodes:
                if not n.is_locked and n.mass > 0:
                    dN = n.dN(x, lp, dx)
                    Lp += dN * n.momentum / n.mass

            p.def_gradient *= (1 + Lp * self.dt)
            p.vol = p.def_gradient * p.init_vol
            dE = self.dt * Lp
            p.strain += dE
            p.stress += p.mat.E * dE

        self.t += self.dt
