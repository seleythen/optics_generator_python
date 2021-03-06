import os
import xml.etree.ElementTree as ET
from xml_parser.approximator_configuration import ApproximatorConfiguration
from data.grid_configuration import CanonicalCoordinatesGridConfiguration
from xml_parser.transport_configuration import TransportConfiguration
from xml_parser.aperture_configuration import ApertureConfiguration


class ApproximatorTrainingConfiguration:
    def __init__(self, approximator_configuration,
                 training_sample_configuration,
                 transport_configuration,
                 apertures_configurations,
                 destination_file_name):
        """
        :type approximator_configuration: ApproximatorConfiguration
        :type training_sample_configuration: CanonicalCoordinatesGridConfiguration
        :type transport_configuration: TransportConfiguration
        :type apertures_configurations: List[ApertureConfiguration]
        :type destination_file_name: str
        """
        self.approximator_configuration = approximator_configuration
        self.training_sample_configuration = training_sample_configuration
        self.transport_configuration = transport_configuration
        self.apertures_configurations = apertures_configurations
        self.destination_file_name = destination_file_name

    @staticmethod
    def get_configuration_from(xml_configuration_object, path_to_folder_with_optic):
        approximator_configuration = ApproximatorConfiguration.get_configuration_from_xml(xml_configuration_object)
        training_sample_configuration = CanonicalCoordinatesGridConfiguration.\
            get_configuration_from_xml_object(xml_configuration_object)
        transport_configuration = TransportConfiguration.get_configuration_from_xml(xml_configuration_object,
                                                                                    path_to_folder_with_optic)
        apertures_configurations = ApertureConfiguration.get_configurations_from_xml(xml_configuration_object)
        destination_file_name = xml_configuration_object.attrib["optics_parametrisation_file"]
        return ApproximatorTrainingConfiguration(approximator_configuration, training_sample_configuration,
                                                 transport_configuration, apertures_configurations,
                                                 destination_file_name)


def __get_xml_configuration_object_from_file(path_to_xml_file):
    tree = ET.parse(path_to_xml_file)  # load configuration from xml file
    return tree.getroot()


def get_approximator_configurations_from(path_to_xml_file):
    path_to_folder_with_optic = os.path.split(path_to_xml_file)[0]
    configurations = __get_xml_configuration_object_from_file(path_to_xml_file)
    approximator_configurations = [ApproximatorTrainingConfiguration.get_configuration_from(configuration,
                                                                                            path_to_folder_with_optic)
                                   for configuration in configurations]
    return approximator_configurations
