import argparse
import logging

parser = argparse.ArgumentParser(description="Generator plots of optical functions")
parser.add_argument("path to xml", metavar='path', type=str, help="Path to xml file")
parser.add_argument("name of folder with plots", metavar='folder name', type=str, help="Name of folder where plots will be stored")
parser.add_argument("-v", "--verbose", dest='logging-level', action='store_const', const=logging.DEBUG, default=logging.INFO, help="Verbosity of program, if set, logs from madx will be created")
args = parser.parse_args()

logger = logging.getLogger()
logger.setLevel(getattr(args, "logging-level"))


import data.grid_configuration as grid_configuration_module
import os
import shutil
import xml_parser.approximator_training_configuration as app_conf
import seaborn as sns
import comparators.transport as transport
import matplotlib.pyplot as plt
from data.parameters_names import ParametersNames as Parameters
from transporters.madx.ptc_track.configuration import PtcTrackConfiguration
from transporters.approximator.configuration import ApproximatorConfiguration

sns.set_style("whitegrid")
path_to_xml_file = getattr(args, "path to xml")
path_to_optic = os.path.split(path_to_xml_file)[0]
output_dir = getattr(args, "name of folder with plots")

output_path = os.path.join(output_dir, "Error_plots")
if os.path.isdir(output_path):
    shutil.rmtree(output_path)
os.makedirs(output_path)

configurations = app_conf.get_approximator_configurations_from(path_to_xml_file)

serialized_approximator_file_name = configurations[0].destination_file_name
path_to_approximator = os.path.join(path_to_optic, serialized_approximator_file_name)

transporter1 = "ptc_track"
transporter2 = "approximator"

for configuration in configurations:
    approximator_name = configuration.approximator_configuration.name_of_approximator
    s = configuration.transport_configuration.end_place.distance

    track_configuration = PtcTrackConfiguration.get_track_configuration_from_xml_configuration_object(
        configuration.transport_configuration)
    approximator_configuration = ApproximatorConfiguration(path_to_approximator, approximator_name)

    transporters = {
        transporter1: track_configuration,
        transporter2: approximator_configuration
    }

    test_sample_configuration = configuration.training_sample_configuration
    particles = test_sample_configuration.generate_randomly()

    title_sufix = path_to_optic + "\nError over training scope\n"
    title_sufix += configuration.transport_configuration.end_place.name + "; s = " + str(s)

    stat_path = os.path.join(output_path, "Station_"+str(s))

    if not os.path.isdir(stat_path):
        os.makedirs(stat_path)

    errors = transport.compare(particles, transporters)

    def save_plot_of(transported_parameter, depended_parameter, file_name):
        fig = plt.gcf()
        transport.plot(errors, transported_parameter, depended_parameter, title_sufix=title_sufix)
        fig.savefig(os.path.join(stat_path, file_name + ".jpg"))
        plt.clf()

    file_name_begin = "DELTA"
    save_plot_of(Parameters.X, Parameters.PT, file_name_begin + "_X_vs_PT")
    save_plot_of(Parameters.THETA_X, Parameters.PT, file_name_begin + "_THETA_X_vs_PT")
    save_plot_of(Parameters.Y, Parameters.PT, file_name_begin + "_Y_vs_PT")
    save_plot_of(Parameters.THETA_Y, Parameters.PT, file_name_begin + "_THETA_Y_vs_PT")
