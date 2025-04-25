from numpy import arange, pi, cos, sin, sqrt, ceil, zeros
from material import Material
from domain import Domain
from timeintegration import TimeIntegration

import os

THIS = os.path.basename(__file__).split('.')[0]

if __name__ == '__main__':

    # MATERIAL DATA
    E = 100
    rho = 1

    # GRID DATA
    dx = 1.0
    L = 25.0

    # PARTICLE DATA
    ppe = 2
    v0 = 0.1
    n = 1
    beta = (2 * n - 1) * pi / 2. / L
    c = sqrt(E / rho)
    omega = beta * c
    T = 2. * pi / omega

    # TIME DATA
    t0 = 0
    tf = 100
    pct = 0.1

    # MODEL CREATION
    domain = Domain()

    domain.genGrid(dx, -dx, L + 2 * dx)
    domain.grid.lockNodeAtCoord(0)
    domain.grid.lockNodeAtCoord(-dx)

    material = Material(E, rho)

    domain.genParticles(material, ppe, 0, L)
    for p in domain.particles:
        p.vel = v0 * sin(beta * p.coord)
    #     print(f'{p.id} {p.vel} 0 0')
    # quit()

    # TIME INTEGRATION
    time = TimeIntegration(domain, tf, t0, pct=pct)

    num_steps = (int)(ceil((tf - t0) / time.dt))
    num_print_steps = 100
    step = (int)(ceil(num_steps / num_print_steps))
    step_acc = step
    progress = 100 / num_print_steps

    t = zeros(num_steps)
    vCM = zeros(num_steps)
    M = sum([p.mass for p in time.domain.particles])

    time.initializeParticles()

    for i in range(num_steps):

        if i == 2:
            quit()

        print('----------------------------------------')
        print(f'Time: {time.t}')
        print(f'Time increment: {time.dt}')
        print('----------------------------------------')

        t[i] = time.t
        vCM[i] = sum([p.vel * p.mass for p in time.domain.particles]) / M

        time.usl()

        if i > step_acc:
            print(f'PROGRESS: {round(progress, 2)}%\t|\tTIME: {round(time.t, 4)} s', flush=True)
            progress += 100 / num_print_steps
            step_acc += step

    analytical = [v0 / beta / L * cos(omega * ti) for ti in t]

    import matplotlib.pyplot as plt

    plt.plot(t, analytical, '-', label='Analytical', linewidth=2)
    plt.plot(t, vCM, 'o-', label='GIMPy', linewidth=2)
    plt.legend()
    plt.savefig(f'{THIS}_velocity.pdf')

    # Assert that the analytical solution is correct
    import numpy as np

    relative_error = np.abs([(v - a) / a for v, a in zip(vCM, analytical)])
    relative_error = [e for e in relative_error if e < 1e+6]
    error_avg = np.average(relative_error)
    error_std = np.std(relative_error, dtype=np.float64)
    error_normal = [e for e in relative_error if error_avg - 3 * error_std < e < error_avg + 3 * error_std]
    error = 100.0 * np.average(error_normal)

    print('Relative error (%): ', error)

    print('FINISHED')
