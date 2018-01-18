#!/usr/bin/env python

import sys
from model.model import Model

def main():
	if len(sys.argv) < 3:
		print('Usage: {0} <data_dir> <algorithm_type>'.format(sys.argv[0]))
		return 1

	dataDirectory = sys.argv[1]
	model = Model(dataDirectory)

	try:
		algorithmTypeStr = sys.argv[2]
		algorithmType = Model.AlgorithmType[algorithmTypeStr]
	except KeyError:
		print("Unknown AlgorithmType: {0}".format(algorithmTypeStr))
		return 1

	carsUsage = model.run(algorithmType)
	print(carsUsage)

if __name__ == "__main__":
	main()
