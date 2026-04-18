from scipy.stats import qmc

def sobol_sample(n, x_min, x_max, y_min, y_max):
    sampler = qmc.Sobol(d=2, scramble=True)
    samples = sampler.random(n)

    # scale to your bounds
    l_bounds = [x_min, y_min]
    u_bounds = [x_max, y_max]
    return qmc.scale(samples, l_bounds, u_bounds)

samples = sobol_sample(10, 0, 45.8, 0, 22)
print(samples)