import ROOT
from ROOT import gSystem, gInterpreter
import numpy as np
import os


def get_approximator(path_to_project, path_to_file, approximator_name):
    """
    Get approximator_test from file. Use only once, since it initialize variables in ROOT, so with second use it is going
    to explode. Sorry.
    :param path_to_project: path to optics_generator_python. Needed files from it:
    - properly initialized folder root_libs
    - src/root_classes/include
    :param path_to_file: path to file with serialized LHCOpticsApproximator object
    :param approximator_name: name of approximator_test in ROOT file
    :return: approximator_test object
    """
    os.environ['LD_LIBRARY_PATH'] = path_to_project + "/root_libs"
    gInterpreter.ProcessLine(".include " + path_to_project + "/src/root_classes/include")
    gSystem.Load("LHCOpticsApproximator")
    gInterpreter.ProcessLine('TFile *f=TFile::Open("' + path_to_file + '");')
    gInterpreter.ProcessLine(
        'std::auto_ptr<LHCOpticsApproximator> apr = std::auto_ptr<LHCOpticsApproximator>((LHCOpticsApproximator*) f->Get("' + approximator_name + '"));')
    gInterpreter.ProcessLine("f->Close()")
    gInterpreter.ProcessLine("double input[5];")
    gInterpreter.ProcessLine("double output[5];")
    approximator = ROOT.apr
    return approximator


def transport(approximator, matrix):
    """
    Transport particles described in matrix
    :param approximator: LHCOpticsApproximator object
    :param matrix: each row should contain begining position of particle- x, theta x, y, theta y, pt
    :return: matrix with result of transport, where each row contain x, theta x, y, theta y, t, pt
    """
    # Using such containers is probably the easiest way to work with root objects
    # It will contain input values and output values will be stored in them
    input_container = ROOT.input
    output_container = ROOT.output
    end_positions = list()
    for index, row in enumerate(matrix):
        for i, value in enumerate(row):
            input_container[i] = value
        approximator.Transport(input_container, output_container)
        end_position = []
        for i, value in enumerate(output_container):
            end_position.append(value)
        end_positions.append(end_position)
    return np.array(end_positions)