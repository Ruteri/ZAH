#!/usr/bin/env python

# mapper.py
# Draws points and paths lists into map using Latex TikZ
# Author: akowalew

import sys
import numpy as np

# Collects data from sweep algorithm and draws the map of points in TikZ
def texmap(sweep_result, depot_x, depot_y):
	tex = ("\\documentclass[class=minimal,border=0pt]{standalone}"
		"\\usepackage{tikz}"
		"\\begin{document}"
		"\\begin{tikzpicture}"
	)

	tex += "\\draw[green] ({0}, {1}) circle (0.25)".format(depot_x, depot_y)
	tex += " node {{D}};"

	i = 1
	for (x, y, demand, _, car) in sweep_result:
		tex += "\\draw[blue] ({0}, {1}) circle (0.25)".format(x, y)
		tex += " node {{{0}}}".format(i)
		tex += " node[above=10, right=5, red] {{{0}}};".format(demand)
		i += 1

	tex += ("\\end{tikzpicture}"
		"\\end{document}"
	)

	return tex

def main():
    if len(sys.argv) < 5:
        print("Usage: {0} <sweep_result> <depot_x> <depot_y> <output_texfile>"
        	.format(sys.argv[0]))
        return 1

    sweep_result = np.genfromtxt(sys.argv[1], delimiter=",")
    (depot_x, depot_y) = (float(sys.argv[2]), float(sys.argv[3]))
    output_texfile = sys.argv[4]

    with open(output_texfile, "w") as output:
    	tex = texmap(sweep_result, depot_x, depot_y)
    	output.write(tex)

    return 0

if __name__ == "__main__":
	result = main()
