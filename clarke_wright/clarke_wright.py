#!/usr/bin/env python

import sys
import numpy as np

def clarke_wright(distances, demands, capacity):

    num_of_cities = demands.shape[0]
    city_cycle = np.array(range(0, num_of_cities), dtype='int')

    # Define cycles. For now each consists of a single city
    cycles = []
    for city in range(0, num_of_cities):
        cycles.append(np.array([city], dtype='int'))

    cargo = demands

    # Calculate savings (for each pair of ciities)
    savings = np.array([]).reshape(0,3)
    for i in range(1, num_of_cities):
        for j in range(i + 1, num_of_cities):
            saving = distances[0, i] + distances[0, j] - distances[i, j]
            savings = np.append(savings, [[i, j, saving]], axis=0)

    # Sort savings in decreasing order
    new_order = savings[:, 2].argsort()
    savings = savings[new_order[::-1]]

    for idx, (i, j, saving) in enumerate(savings):

        cycle_i = city_cycle[int(i)]
        cycle_j = city_cycle[int(j)]

        # Make sure cities don't belong to the same cycle
        if cycle_i == cycle_j:
            continue

        # Check if car's capacity is big enough to merge cycles
        if (cargo[cycle_i] + cargo[cycle_j]) > capacity:
            continue

        if cycles[cycle_i][0] == i and cycles[cycle_j][0] == j:
            # Reverse i. Append j to the end of i
            cycles[cycle_i] = cycles[cycle_i][::-1]

        elif cycles[cycle_i][-1] == i and cycles[cycle_j][-1] == j:
            # Reverse j. Append j to the end of i
            cycles[cycle_j] = cycles[cycle_j][::-1]

        elif cycles[cycle_j][0] == j and cycles[cycle_i][-1] == i:
            # Reverse both
            cycles[cycle_i] = cycles[cycle_i][::-1]
            cycles[cycle_j] = cycles[cycle_j][::-1]

        elif cycles[cycle_i][-1] != i or cycles[cycle_j][0] != j:
            # Can't merge
            continue

        # Move all cities form j's cycle to i's cycle
        for city in cycles[cycle_j]:
            city_cycle[city] = cycle_i

        # Merge cycles
        cycles[cycle_i] = np.append(cycles[cycle_i], cycles[cycle_j])
        cycles[cycle_j] = np.array([])

        # Update cargos
        cargo[cycle_i] += cargo[cycle_j]
        cargo[cycle_j] = 0

    return (cycles, city_cycle, cargo)

# Calculates simplified demand as total volume of products needed to fulfill
# the demand
def get_simplified_demand(demand, volumes):

    simplified_demand = np.zeros((demand.shape[0], 1))

    for idx0, row in enumerate(demand):
        overall_volume = 0
        for idx1, elem in enumerate(row):
            overall_volume += elem * volumes[idx1]
        simplified_demand[idx0] = overall_volume

    return simplified_demand

def main():

    distances = np.genfromtxt('../example2/roads', delimiter=",")
    demand = np.genfromtxt('../example2/demand', delimiter=",")
    volumes = np.genfromtxt('../example2/volumes')
    capacity = np.genfromtxt('../example2/capacity')

    demand = get_simplified_demand(demand, volumes)

    (cycles, city_cycle, cargo) = clarke_wright(distances, demand, 2000)

    print('\nCycles as vectors (possibly empty):')
    print(cycles)

    print('\nCycles assigned to each city:')
    print(city_cycle)

    print('\nCargo in each cycle (possibly zero):')
    print(cargo)

if __name__ == "__main__":
    main()
