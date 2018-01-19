#!/usr/bin/env python

import sys
from model.model import Model
import numpy as np
from datetime import datetime

def print_green(x):
	print('\033[92m\033[1m' + x + '\033[0m')

def print_texmap_data(output_dir, carsUsage, points):

	f = open('{0}/points'.format(output_dir), 'w')
	for point in points:
		f.write(", ".join(str(x) for x in point) + "\n")
	f.close()

	f = open('{0}/paths'.format(output_dir), 'w')
	for car in carsUsage:
		if len(car.path) > 1:
			f.write(", ".join(str(x) for x in car.path[1:]) + "\n")
	f.close()

def main():
	if len(sys.argv) < 3:
		print('Usage: {0} data_dir algorithm_type [output_dir]'.format(sys.argv[0]))
		return 1

	dataDirectory = sys.argv[1]
	model = Model(dataDirectory)

	try:
		algorithmTypeStr = sys.argv[2]
		algorithmType = Model.AlgorithmType[algorithmTypeStr]
	except KeyError:
		print("Unknown AlgorithmType: {0}".format(algorithmTypeStr))
		return 1

	start = datetime.now()

	carsUsage, points = model.run(algorithmType)

	end = datetime.now()

	print(carsUsage)

	print_green('Elapsed time (hh:mm:ss.ms): {0}'.format(end - start))

	if len(sys.argv) > 3:
		output_dir = sys.argv[3]
		print_texmap_data(output_dir, carsUsage, points)

if __name__ == "__main__":
	main()
