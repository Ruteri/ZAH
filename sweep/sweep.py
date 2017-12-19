#!/usr/bin/env python

import sys
import numpy as np
from math import atan2, pi

def sweep(points, car_capacities, depot_coordinates):
    clusters = []
    current_car = 0

    depot_x = depot_coordinates[0]
    depot_y = depot_coordinates[1]

    # Compute angle coordinate (in polar coordinates) of each point with respect
    # to the depot
    angles = []
    for (point_x, point_y, demand) in points:

        # Calculate coordinates relatively to the depot
        rel_x = point_x - depot_x
        rel_y = point_y - depot_y

        # Calculate angle
        angle = atan2(rel_y, rel_x)
        angles.append(angle)

    # Add columns with angles and cluster assignment
    points = np.append(points, np.transpose(np.array(angles, ndmin=2)), axis=1)
    points = np.append(points, np.zeros((points.shape[0], 1)), axis=1)

    # Sort points by angle (fourth column, hence [:,3])
    points[points[:,3].argsort()]

    # Assign to clusters
    current_car = 0
    current_cargo = 0
    current_capacity = car_capacities[current_car]
    for idx, (_, _, demand, _, _) in enumerate(points):

        # Check if we can fit all the cargo into the current car
        if current_cargo + demand > current_capacity:

            # Switch to the next car making sure it is big enough
            current_car += 1
            while current_car < car_capacities.shape[0] and car_capacities[current_car] < demand:
                current_car += 1

            if current_car >= car_capacities.shape[0]:
                print("Warning: All remaining cars are too small to fulfill the demand")
                break

            current_cargo = 0
            current_capacity = car_capacities[current_car]

        # Increase cargo in current car
        current_cargo += demand

        # Assign to current cluster (car)
        points[idx][4] = current_car

    return points

def main():

    if len(sys.argv) < 5:
        print('Usage: {0} <points_filename> <cars_filename> <depot_x> <depot_y>'.format(sys.argv[0]))
        return 1

    points = np.genfromtxt(sys.argv[1],delimiter=",")
    cars = np.genfromtxt(sys.argv[2])
    depot_coordinates = (float(sys.argv[3]), float(sys.argv[4]))

    points = sweep(points, cars, depot_coordinates)

    for (x, y, demand, angle, car) in points:
        print("{0: >8},{1: >8},{2: >10},{3: >20},{4: >2}".format(x, y, demand, angle, int(car)))

if __name__ == "__main__":
    main()
