import transporters.approximator.optical_functions as aop
import transporters.madx.ptc_track.optical_functions as mop
import numpy as np
import visualization.visualize as visualizer
import seaborn as sns
from data.parameters_names import ParametersNames as Parameters


def compare_d_x(bunch_configuration, approximator, madx_configuration):
    position_with_difference = compare_two(bunch_configuration, approximator, aop.compute_d_x, madx_configuration,
                                           mop.compute_d_x)

    return position_with_difference


def compare_d_y(bunch_configuration, approximator, madx_configuration):
    position_with_difference = compare_two(bunch_configuration, approximator, aop.compute_d_y, madx_configuration,
                                           mop.compute_d_y)

    return position_with_difference


def compare_l_x(bunch_configuration, approximator, madx_configuration):
    position_with_difference = compare_two(bunch_configuration, approximator, aop.compute_l_x, madx_configuration,
                                           mop.compute_l_x)

    return position_with_difference


def compare_l_y(bunch_configuration, approximator, madx_configuration):
    position_with_difference = compare_two(bunch_configuration, approximator, aop.compute_l_y, madx_configuration,
                                           mop.compute_l_y)

    return position_with_difference


def compare_v_x(bunch_configuration, approximator, madx_configuration):

    position_with_difference = compare_two(bunch_configuration, approximator, aop.compute_v_x, madx_configuration,
                                           mop.compute_v_x)

    return position_with_difference


def compare_v_y(bunch_configuration, approximator, madx_configuration):

    position_with_difference = compare_two(bunch_configuration, approximator, aop.compute_v_y, madx_configuration, mop.compute_v_y)

    return position_with_difference


def compare_two(bunch_configuration, transporter1, optical_function_of_transporter1,
                transporter2, optical_function_of_transporter2):
    approximator_result = optical_function_of_transporter1(transporter1, bunch_configuration)
    madx_result = optical_function_of_transporter2(transporter2, bunch_configuration)

    approximator_v_x = approximator_result.T[5]
    madx_v_x = madx_result.T[5]

    approximator_result.T[5] = (approximator_v_x - madx_v_x)

    return approximator_result


def compute_norm(diff, values, madx_matrix, approximator_matrix):
    relative_diff = np.divide(diff, values.reshape((-1, 1)))
    abs_val_of__rel_diff = np.absolute(relative_diff)
    max_diff = np.max(abs_val_of__rel_diff)
    return abs_val_of__rel_diff, madx_matrix, approximator_matrix


def compare_all(bunch_configuration, approximator, madx_configuration):
    return {
        Parameters.D_X: compare_d_x(bunch_configuration, approximator, madx_configuration),
        Parameters.D_Y: compare_d_y(bunch_configuration, approximator, madx_configuration),
        Parameters.L_X: compare_l_x(bunch_configuration, approximator, madx_configuration),
        Parameters.L_Y: compare_l_y(bunch_configuration, approximator, madx_configuration),
        Parameters.V_X: compare_v_x(bunch_configuration, approximator, madx_configuration),
        Parameters.V_Y: compare_v_y(bunch_configuration, approximator, madx_configuration)
    }


def visualize_diff(differences_with_position, parameter_name, optical_function_name):
    mapping = {
        Parameters.X: 0,
        Parameters.THETA_X: 1,
        Parameters.Y: 2,
        Parameters.THETA_Y: 3,
        Parameters.PT: 4,
        optical_function_name: 5
    }
    axes = visualizer.plot_from_one_matrix(parameter_name, optical_function_name, differences_with_position, mapping,
                                           plot_function=sns.scatterplot)
    return axes


def visualize_diff_d_x(bunch_configuration, approximator, madx_configuration, parameter_name):
    differences = compare_d_x(bunch_configuration, approximator, madx_configuration)
    return visualize_diff(differences, parameter_name, Parameters.D_X)


def visualize_diff_d_y(bunch_configuration, approximator, madx_configuration, parameter_name):
    differences = compare_d_y(bunch_configuration, approximator, madx_configuration)
    return visualize_diff(differences, parameter_name, Parameters.D_Y)


def visualize_diff_l_x(bunch_configuration, approximator, madx_configuration, parameter_name):
    differences = compare_l_x(bunch_configuration, approximator, madx_configuration)
    return visualize_diff(differences, parameter_name, Parameters.L_X)


def visualize_diff_l_y(bunch_configuration, approximator, madx_configuration, parameter_name):
    differences = compare_l_y(bunch_configuration, approximator, madx_configuration)
    return visualize_diff(differences, parameter_name, Parameters.L_Y)


def visualize_diff_v_x(bunch_configuration, approximator, madx_configuration, parameter_name):
    differences = compare_v_x(bunch_configuration, approximator, madx_configuration)
    return visualize_diff(differences, parameter_name, Parameters.V_X)


def visualize_diff_v_y(bunch_configuration, approximator, madx_configuration, parameter_name):
    differences = compare_v_y(bunch_configuration, approximator, madx_configuration)
    return visualize_diff(differences, parameter_name, Parameters.V_Y)
