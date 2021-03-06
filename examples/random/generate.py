#!/usr/bin/env python

import sys
import math
import numpy as np

def gen_int_data_file(name, dim, range):
    data = np.random.randint(range[0], range[1], dim)
    np.savetxt(name, data, delimiter=',', fmt='%d')
    return data

def gen_float_data_file(name, dim, max):
    data = np.multiply(np.random.rand(dim[0], dim[1]), max)
    np.savetxt(name, data, delimiter=',')

def main():
    
    if len(sys.argv) < 3:
        print('Usage: {0} num_of_cities output_dir'.format(sys.argv[0]))
        return 1

    num_of_cities = int(sys.argv[1])
    num_of_cars = num_of_cities

    output_dir = sys.argv[2]

    gen_int_data_file(output_dir + '/capacity', [num_of_cars, 1], [10000, 14000])
    gen_int_data_file(output_dir + '/demand', [num_of_cities, 3], [100, 300])
    gen_int_data_file(output_dir + '/prices', [num_of_cities, 3], [1, 10])
    #gen_int_data_file('roads', [num_of_cities, num_of_cities], [1, 2000])
    gen_float_data_file(output_dir + '/shortage_coeff', [num_of_cities, 3], 5)
    gen_int_data_file(output_dir + '/supply', [3, 1], [301*num_of_cities, 400*num_of_cities])
    gen_int_data_file(output_dir + '/volumes', [3, 1], [1, 5])

    coordinates = gen_int_data_file(output_dir + '/coordinates', [num_of_cities, 2], [0, 500])

    roads = np.zeros([num_of_cities, num_of_cities])
    for i in range(0, num_of_cities):
        roads[i,i] = 99999;
        for j in range(i+1, num_of_cities):
            xi = coordinates[i,0]
            yi = coordinates[i,1]
            xj = coordinates[j,0]
            yj = coordinates[j,1]
            dx = xi - xj
            dy = yi - yj
            roads[i,j] = roads[j,i] = math.sqrt(dx*dx + dy*dy)
    np.savetxt(output_dir + '/roads', roads, delimiter=',')

    f = open(output_dir + '/cities', 'w')
    for i in range(0, num_of_cities):
        f.write("m\n")
    f.close()


if __name__ == "__main__":
    main()