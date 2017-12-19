#!/usr/bin/env python

# mapper.py
# Draws points and paths lists into map using Latex TikZ
# Author: akowalew

import sys
import numpy as np

# Collects data from sweep algorithm and draws the map of points in TikZ
def texmap(points, paths, depot_x, depot_y):
	tex = ("\\documentclass[border=0pt]{standalone}\n"
		"\\usepackage{tikz}\n"
		"\\usetikzlibrary{arrows.meta}"
		"\\usetikzlibrary{colorbrewer}"
		"\\begin{document}\n"
		"\\begin{tikzpicture}\n"
		"\\tikzstyle{every node}=[font=\\tiny]"
	)

	tex += "\\draw[green] ({0}, {1}) circle (0.04)\n".format(depot_x/100, depot_y/100)
	tex += " node[scale=0.15] {{D}};\n"

	i = 1
	for (x, y, demand) in points:
		tex += "\\draw[blue, ultra thin] ({0}, {1}) circle (0.04)\n".format(x/100, y/100)
		tex += " node[scale=0.2, above=-2.5] {{{0}}}\n".format(i)
		tex += " node[scale=0.15, below=-1.5, red] {{{0}}};\n".format(int(demand))
		tex += ";"
		i += 1

	colors = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
	color_idx = 0;

	for path in paths:
		tex += "\\draw[ultra thin, arrows=-{{Latex[length=0.75]}}, shorten >=1, shorten <=1, densely dotted] ({0}, {1})\n".format(depot_x/100, depot_y/100)
		last_city = path[-1]

		for city in path:
			idx = city - 1
			(x, y, _) = points[idx]
			tex += " to[] ({0}, {1});\n".format(x/100, y/100)

			if(city == last_city):
				optional_args = ", densely dotted"
			else:
				optional_args = ", draw=Set1-{0}".format(colors[color_idx])
				

			tex += "\\draw[ultra thin, arrows=-{{Latex[length=0.75]}}, shorten >=1, shorten <=1 {0}] ({1}, {2})\n".format(optional_args, x/100, y/100)
		tex += " to[] ({0}, {1});\n".format(depot_x/100, depot_y/100)

		color_idx = (color_idx + 1) % len(colors)

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
