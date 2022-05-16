from numpy import arange, pi, cos, sin, sqrt, ceil, zeros
from material import Material
from domain import Domain
from timeintegration import TimeIntegration

if __name__ == '__main__':

    # MATERIAL DATA
    E = 200.0e9
    rho = 7800.0

    # GRID DATA
    dx = 1.0
    L = 25.0

    # PARTICLE DATA
    ppe = 2
    v0 = .1
    n = 1
    beta = (2*n-1)*pi/2./L
    c = sqrt(E/rho)
    omega = beta * c
    T = 2.*pi/omega

    # TIME DATA
    t0 = 0
    tf = 5*T
    pct = 0.1

    # MODEL CREATION
    domain = Domain()

    domain.genGrid(dx, -dx, L+2*dx)
    domain.grid.lockNodeAtCoord(0)
    domain.grid.lockNodeAtCoord(-dx)

    material = Material(E, rho)

    domain.genParticles(material, ppe, 0, L)
    for p in domain.particles: p.vel = v0*sin(beta*p.coord)

    # TIME INTEGRATION
    time = TimeIntegration(domain, tf, t0, pct=pct)

    num_steps = (int) ( ceil((tf-t0)/time.dt) )
    num_print_steps = 100
    step = (int) ( ceil(num_steps / num_print_steps) )
    step_acc = step
    progress = 100/num_print_steps
    
    t = zeros(num_steps)
    vCM = zeros(num_steps)
    M = sum([p.mass for p in time.domain.particles])

    for i in range(num_steps): 

        t[i] = time.t
        vCM[i] = sum([p.vel*p.mass for p in time.domain.particles])

        time.advance()

        if i > step_acc:
            print(f'PROGRESS: {round(progress,2)}%\t|\tTIME: {round(time.t,4)} s', flush=True)
            progress += 100/num_print_steps
            step_acc += step

    vCM = [v/M for v in vCM]
    analytical = [v0/beta/L*cos(omega*ti) for ti in t]

    import matplotlib.pyplot as plt

    plt.plot(t, analytical, linewidth=10, label='Analytical')
    plt.plot(t, vCM, 'o-', label='GIMPy')
    plt.legend()
    plt.show()

    print('FINISHED')