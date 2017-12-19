#!/usr/bin/env python

import sys
import tempfile
import numpy as np
from amplpy import AMPL

class Struct(object): pass

def print_scalar_param(file, param, name):
    file.write('param {0} := {1};'.format(name, param))

def print_1d_param(file, param, name):

    # Write header
    file.write('param {0} :=\n'.format(name))

    # Write data rows
    for idx, elem in enumerate(param):
        if isinstance(elem, basestring):
            file.write('{0} "{1}"'.format(idx + 1, elem))
        else:
            file.write('{0} {1}'.format(idx + 1, elem))
        if idx == (param.shape[0] - 1):
            file.write(';')
        file.write('\n')

def print_2d_param(file, param, name):

    # Write header
    file.write('param {0} : '.format(name))
    for i in range(0, param.shape[1]):
        file.write('{0} '.format(i + 1))
    file.write(':=\n')

    # Write data rows
    for idx, row in enumerate(param):
        file.write('{0} '.format(idx + 1))
        for elem in row:
            file.write('{0} '.format(elem))
        if idx == (param.shape[0] - 1):
            file.write(';')
        file.write('\n')

def generate_temp_data_file(data):

    tmp_file = tempfile.NamedTemporaryFile()

    # Fill with data
    print_2d_param(tmp_file, data.demand, 'POPYT')
    print_2d_param(tmp_file, data.prices, 'CENA')
    print_2d_param(tmp_file, data.roads, 'DROGI')
    print_2d_param(tmp_file, data.shortage_coeff, 'WAGA_NIEZADOWOLENIA')
    print_1d_param(tmp_file, data.supply, 'PODAZ')
    print_1d_param(tmp_file, data.volumes, 'OBJETOSC')
    print_1d_param(tmp_file, data.cities, ': punkty: miasta')
    print_1d_param(tmp_file, data.types, ': pieczywa: typy')
    print_scalar_param(tmp_file, 1, 'KOSZT_KIEROWCY')
    print_scalar_param(tmp_file, data.capacity, 'POJEMNOSC')

    # Dirty hack
    # File will be already open while amplpy uses it, but we have to make sure
    # it is 'rewinded'
    tmp_file.seek(0)

    return tmp_file

def run_ampl_model(data):

    # Intiialize AMPL and choose solver
    ampl = AMPL()
    ampl.eval('option solver cplex;')

    # Load model
    ampl.read('ampl/model.mod')

    # Generate and load temporary data file
    data_file = generate_temp_data_file(data)
    ampl.readData(data_file.name)
    data_file.close()

    ampl.solve()

def load_data(data_dir):

    # Load numerical data
    data = Struct()
    data.demand = np.genfromtxt('{0}/demand'.format(data_dir), delimiter=",")
    data.supply = np.genfromtxt('{0}/supply'.format(data_dir), delimiter=",")
    data.prices = np.genfromtxt('{0}/prices'.format(data_dir), delimiter=",")
    data.roads = np.genfromtxt('{0}/roads'.format(data_dir), delimiter=",")
    data.shortage_coeff = np.genfromtxt('{0}/shortage_coeff'.format(data_dir), delimiter=",")
    data.capacity = np.genfromtxt('{0}/capacity'.format(data_dir), delimiter=",")
    data.volumes = np.genfromtxt('{0}/volumes'.format(data_dir), delimiter=",")
    data.points = np.genfromtxt('{0}/volumes'.format(data_dir), delimiter=",")

    # Load textual data
    data.cities = np.array([line.rstrip('\n') for line in open('{0}/cities'.format(data_dir))])
    data.types = np.array([line.rstrip('\n') for line in open('{0}/types'.format(data_dir))])

    return data

def main():

    if len(sys.argv) < 2:
        print('Usage: {0} <data_dir>'.format(sys.argv[0]))
        return 1

    data = load_data(sys.argv[1])

    run_ampl_model(data)

if __name__ == "__main__":
    main()
