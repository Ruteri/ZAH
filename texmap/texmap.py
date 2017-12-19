#!/usr/bin/env python

# mapper.py
# Draws points and paths lists into map using Latex TikZ
# Author: akowalew

import sys
import numpy as np

# Collects data from sweep algorithm and draws the map of points in TikZ
def texmap(points, paths, depot_x, depot_y):
	tex = ("\\documentclass[class=minimal,border=0pt]{standalone}\n"
		"\\usepackage{tikz}\n"
		"\\begin{document}\n"
		"\\begin{tikzpicture}\n"
	)

	tex += "\\draw[green] ({0}, {1}) circle (0.25)\n".format(depot_x, depot_y)
	tex += " node {{D}};\n"

	i = 1
	for (x, y, demand) in points:
		tex += "\\draw[blue] ({0}, {1}) circle (0.25)\n".format(x, y)
		tex += " node {{{0}}}\n".format(i)
		tex += " node[above=10, right=5, red] {{{0}}};\n".format(demand)
		i += 1

	for path in paths:
		tex += "\\draw[thick, ->] ({0}, {1})\n".format(depot_x, depot_y)
		for city in path:
			idx = city - 1
			(x, y, _) = points[idx]
			tex += " to[bend right] ({0}, {1});\n".format(x, y)
			tex += "\\draw[thick, ->] ({0}, {1})\n".format(x, y)
		tex += " to[bend right] ({0}, {1});\n".format(depot_x, depot_y)

	tex += ("\\end{tikzpicture}\n"
		"\\end{document}\n"
	)

	return tex

def read_paths(paths_file):
	with open(paths_file, "r") as file:
		content = file.read()
		lines = content.split("\n")
		paths = []
		for line in lines:
			cities = [int(x) for x in line.split(',')]
			paths.append(cities)

		return paths

def main():
    if len(sys.argv) < 6:
        print("Usage: {0} <points_file> <paths_file> <depot_x> <depot_y> <output_texfile>"
        	.format(sys.argv[0]))
        return 1

    points = np.genfromtxt(sys.argv[1], delimiter=",")
    paths = read_paths(sys.argv[2])
    (depot_x, depot_y) = (float(sys.argv[3]), float(sys.argv[4]))
    output_texfile = sys.argv[5]

    with open(output_texfile, "w") as output:
    	tex = texmap(points, paths, depot_x, depot_y)
    	output.write(tex)

    return 0

if __name__ == "__main__":
	result = main()
