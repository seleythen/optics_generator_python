import data.particles_generator as pg
import madx.runner as mr
import numpy as np


def generate_random_particles(bunch_configuration, path_to_accelerator_configuration, target):
    """
    Generate dict with matrix of particles' parameters on stations. List of stations is in madx configuration generator.
    Take angles into account.
    :param bunch_configuration: dict with beam parameters- x, theta x, y, theta y, t, and pt- their min and max values.
    :param path_to_accelerator_configuration: path to folder with configuration of accelerator. Needed files:
    todo
    :param target: target number of parameters at end station.
    :return: dict with numpy matrix of particles' parameters on stations, matrix format:
    ordinal number, turn, x, theta x, y, theta y, t, pt, e, s, angle x, angle y
    """
    segments = {}
    counter = 0
    number_of_particles_in_one_run = bunch_configuration.get_number_of_particles()

    while ("end" not in segments.keys()) or ("end" in segments.keys() and len(segments["end"]) < target):
        new_particles = __generate_random_particles(bunch_configuration, path_to_accelerator_configuration)

        shift = counter * number_of_particles_in_one_run
        counter += 1
        new_particles = mr.shift_ordinal_number_in_segments(new_particles, shift)

        segments = mr.merge_segments(segments, new_particles)

    return segments


def __generate_random_particles(bunch_configuration, path_to_accelerator_configuration):
    """
    Generate dict with matrix of particles' parameters on stations. List of stations is in madx configuration generator.
    :param bunch_configuration: dict with beam parameters- x, theta x, y, theta y, t, and pt- their min and max values.
    :param path_to_accelerator_configuration: path to folder with configuration of accelerator. Needed files:
    todo
    :return: dict with numpy matrix of particles' parameters on stations, matrix format:
    ordinal number, turn, x, theta x, y, theta y, t, pt, e, s, angle x, angle y
    """
    particles = pg.generate_particles_randomly(bunch_configuration)

    segments = __transport(particles, path_to_accelerator_configuration)

    return segments


def generate_from_range(bunch_configuration, path_to_accelerator_configuration):
    """
    Generate dict with matrices of particles' parameters on stations. List of stations is in madx configuration generator.
    :param bunch_configuration: dict with beam parameters- x, theta x, y, theta y, t, and pt- their min and max values
    :param path_to_accelerator_configuration: path to folder with configuration of accelerator. Needed files:
    todo
    :return: dict with numpy matrix of particles' parameters on stations, matrix format:
    ordinal number, turn, x, theta x, y, theta y, t, pt, e, s, angle x, angle y
    """

    particles = pg.generate_from_range(bunch_configuration)

    segments = __transport(particles.T, path_to_accelerator_configuration)

    return segments


def __transport(particles, path_to_accelerator_configuration):
    """
    Transport particles described in matrix. Matrix format: x, theta x, y, theta y, t, pt
    :param particles:
    :param path_to_accelerator_configuration:
    :return: dict with matrices describing position of particles on stations, matrix format:
    ordinal number, turn, x, theta x, y, theta y, t, pt, e, s
    """
    number_of_processes = 4
    segments = mr.compute_trajectory(particles, path_to_accelerator_configuration, number_of_processes)

    return segments



