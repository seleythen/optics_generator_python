import numpy as np
from data.parameters_names import ParametersNames as Parameters
from data.particles import Particles
"""
File include some methods to generate matrix with parameters of particles.
There is two ways generating:
- random with values from given range
- with given step from given range
"""


def get_mapping():
    mapping = {
        Parameters.X: 0,
        Parameters.THETA_X: 1,
        Parameters.Y: 2,
        Parameters.THETA_Y: 3,
        Parameters.CROSSING_ANGLE: 4,
        Parameters.PT: 5,
    }
    return mapping


def generate_from_range(grid_configuration):
    """
    Generate carthesian product of parameters of given range.
    :param: GridConfiguration grid_configuration
    :return:
    """
    # Create and initialize vectors with coordinates of particles in grid
    conf = grid_configuration
    x_vector = np.linspace(conf.x_min, conf.x_max, conf.x_resolution)
    theta_x_vector = np.linspace(conf.theta_x_min, conf.theta_x_max, conf.theta_x_resolution)
    y_vector = np.linspace(conf.y_min, conf.y_max, conf.y_resolution)
    theta_y_vector = np.linspace(conf.theta_y_min, conf.theta_y_max, conf.theta_y_resolution)
    xa_vector = np.linspace(conf.xa_min, conf.xa_max, conf.xa_resolution)
    pt_vector = np.linspace(conf.pt_min, conf.pt_max, conf.pt_resolution)

    # Create grid, which is carthesian product of above coordinates vectors
    grid = np.array(np.meshgrid(x_vector, theta_x_vector, y_vector, theta_y_vector, xa_vector, pt_vector))\
        .T.reshape(-1, 6)

    particles_object = Particles(grid, get_mapping())

    return particles_object


def generate_particles_randomly(grid_configuration):
    """
    Generate matrix with random values of parameters from given ranges
    :param grid_configuration
    :return: numpy matrix with number_of_particles x 5 shape
    """
    min_resolution = [grid_configuration.x_min, grid_configuration.theta_x_min, grid_configuration.y_min,
                      grid_configuration.theta_y_min, grid_configuration.xa_min, grid_configuration.pt_min]
    max_resolution = [grid_configuration.x_max, grid_configuration.theta_x_max, grid_configuration.y_max,
                      grid_configuration.theta_y_max, grid_configuration.xa_max, grid_configuration.pt_max]

    number_of_parameters = 6
    number_of_particles = grid_configuration.get_number_of_particles()

    max_vector = np.zeros((1, number_of_parameters))
    min_vector = np.zeros((1, number_of_parameters))

    # TODO refactor
    for i in range(number_of_parameters):
        max_vector[0][i] = max_resolution[i]
        min_vector[0][i] = min_resolution[i]

    grid = (max_vector - min_vector) * np.random.random_sample((number_of_particles, number_of_parameters)) + min_vector
    return grid
