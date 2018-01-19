#!/usr/bin/env python

import sys
from model.model import Model
import numpy as np

def print_texmap_data(output_dir, carsUsage, points):

	# Remove bakery/depot from the list of points
	points = points[1:]

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

	carsUsage, points = model.run(algorithmType)
	print(carsUsage)

	if len(sys.argv) > 3:
		output_dir = sys.argv[3]
		print_texmap_data(output_dir, carsUsage, points)

if __name__ == "__main__":
	main()
