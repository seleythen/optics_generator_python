import madx_runner as mr
import particles_generator as pg
import os
import shutil
"""
Module include functions to obtain parameters of optics such like dispersion or magnetism.
They are calculated using madx to obtain particle trajectory and then they are obtained using numerical derivative.
"""


def compute_l_y(x, theta_x, y, theta_y, ksi, delta_theta=0.000001):
    particle1 = get_one_particle(x, theta_x, y, theta_y, ksi)
    particle1_attributes = process_row(particle1)
    particle2 = get_one_particle(x, theta_x, y, theta_y + delta_theta, ksi)
    particle2_attributes = process_row(particle2)
    return (particle2_attributes["y"] - particle1_attributes["y"]) / delta_theta


def compute_l_x(x, theta_x, y, theta_y, ksi, delta_theta=0.000001):
    particle1 = get_one_particle(x, theta_x, y, theta_y, ksi)
    particle1_attributes = process_row(particle1)
    particle2 = get_one_particle(x, theta_x, y, theta_y + delta_theta, ksi)
    particle2_attributes = process_row(particle2)
    return (particle2_attributes["y"] - particle1_attributes["y"]) / delta_theta


def get_one_particle(x, theta_x, y, theta_y, ksi):
    bunch_size = 1
    current_path = os.getcwd()
    folder_name = "kali1234"
    # os.rmdir(folder_name)
    os.mkdir(folder_name)
    os.chdir(folder_name)

    with open("ready_config", "w") as output_file:
        with open(
                "/home/rafalmucha/Pobrane/optic/optics_generator_python/src/parameters_generator/configuration.madx") as input_file:
            output_file.write("bunch_size = " + str(bunch_size) + ";\n")
            output_file.write("DELTA_AP = " + str(ksi) + ";\n")
            for i in input_file:
                output_file.write(i)

    pg.generate_from_range(x, x, bunch_size,
                           theta_x, theta_x, 1,
                           y, y, 1,
                           theta_y, theta_y, 1,
                           0, 0, 1,
                           ksi, ksi, 1)

    mr.run_madx("ready_config")
    segments = mr.read_in_madx_output_file("trackone")

    matrix = segments["end"]

    os.chdir(current_path)
    shutil.rmtree(folder_name)

    return matrix[0]


def process_row(row):
    mapping = {
        "number": row[0],
        "turn"  : row[1],
        "x"     : row[2],
        "theta_x" : row[3],
        "y"     : row[4],
        "theta_y" : row[5],
        "t"     : row[6],
        "pt"    : row[7],
        "s"     : row[8],
        "e"     : row[9]
    }
    return mapping
