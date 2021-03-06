import sys
import tempfile
import numpy as np
from copy import deepcopy
from amplpy import AMPL
from sweep.sweep import sweep
from clarke_wright.clarke_wright import clarke_wright
from collections import namedtuple
from enum import Enum

class Model(object):
	Result = namedtuple("Result", "carId cargo sales road path income totalIncome capacityUsed")

	class AlgorithmType(Enum):
		Sweep = 1
		ClarkeWright = 2

	def __init__(self, dataDirectory, verbose=False):
		self.data = self.load_data(dataDirectory)
		print("Loaded data: {0}".format(self.data))
		self.verbose = verbose

	def run(self, algorithmType):
		if algorithmType is Model.AlgorithmType.Sweep:
			result = self.run_sweep(self.data)
		elif algorithmType is Model.AlgorithmType.ClarkeWright:
			result = self.run_clarke_wright(self.data)
		else:
			raise ValueError("algorithmType is invalid: {0}".format(algorithmType))

		# Run AMPL model for each car separately
		results = []
		for (car_id, cities) in result:

			if self.verbose:
				print('\nCAR {0}:'.format(car_id))

			# Get subset of the data and run AMPL model
			data_subset = self.get_data_subset(self.data, car_id, cities)
			ampl = self.run_ampl_model(data_subset)

			result = self.collectResult(car_id, ampl, cities)
			results.append(result)

			if self.verbose:
				print(result)

		simplified_demand = self.get_simplified_demand(self.data.demand, self.data.volumes)
		points = np.append(self.data.coordinates, simplified_demand, axis=1)

		return results, points

	def print_scalar_param(self, file, param, name):
		file.write(b'param {0} := {1};'.format(name, param))

	def print_1d_param(self, file, param, name):

		# Write header
		file.write(b'param {0} :=\n'.format(name))

		# Write data rows
		for idx, elem in enumerate(param):
			if isinstance(elem, basestring):
				file.write(b'{0} "{1}"'.format(idx + 1, elem))
			else:
				file.write(b'{0} {1}'.format(idx + 1, elem))
			if idx == (param.shape[0] - 1):
				file.write(b';')
			file.write(b'\n')

	def print_2d_param(self, file, param, name):

		# Write header
		file.write(b'param {0} : '.format(name))
		for i in range(0, param.shape[1]):
			file.write(b'{0} '.format(i + 1))
		file.write(b':=\n')

		# Write data rows
		for idx, row in enumerate(param):
			file.write(b'{0} '.format(idx + 1))
			for elem in row:
				file.write(b'{0} '.format(elem))
			if idx == (param.shape[0] - 1):
				file.write(b';')
			file.write(b'\n')

	def write_data_to_temp_file(self, tmp_file, data):
		self.print_2d_param(tmp_file, data.demand, 'POPYT')
		self.print_2d_param(tmp_file, data.prices, 'CENA')
		self.print_2d_param(tmp_file, data.roads, 'DROGI')
		self.print_2d_param(tmp_file, data.shortage_coeff, 'WAGA_NIEZADOWOLENIA')
		self.print_1d_param(tmp_file, data.supply, 'PODAZ')
		self.print_1d_param(tmp_file, data.volumes, 'OBJETOSC')
		self.print_1d_param(tmp_file, data.cities, ': punkty: miasta')
		self.print_1d_param(tmp_file, data.breadTypes, ': pieczywa: typy')
		self.print_scalar_param(tmp_file, 1, 'KOSZT_KIEROWCY')
		self.print_scalar_param(tmp_file, data.capacity, 'POJEMNOSC')

	def generate_temp_data_file(self, data):
		tmp_file = tempfile.NamedTemporaryFile()

		# Fill with data
		self.write_data_to_temp_file(tmp_file, data)
		if self.verbose:
			print('\nDATA FILE:')
			self.write_data_to_temp_file(sys.stdout, data)
			print('\n')

		# Dirty hack
		# File will be already open while amplpy uses it, but we have to make sure
		# it is 'rewinded'
		tmp_file.seek(0)

		return tmp_file

	def run_ampl_model(self, data):
		# Intiialize AMPL choose solver and load model
		ampl = AMPL()
		ampl.eval('option solver cplex;')
		ampl.read('model/ampl/model.mod')

		# Generate and load temporary data file
		data_file = self.generate_temp_data_file(data)
		ampl.readData(data_file.name)
		data_file.close()

		ampl.solve()
		return ampl

	def findPathInRoad(self, cities, road):
		path = []
		current_city = 0
		while True:
			if current_city == 0 and len(path) > 0:
				break
			path.append(current_city)
			row = road[current_city, :]
			for idx, elem in enumerate(row):
				if elem > 0:
					current_city = idx
					break

		return cities[path]

	def calculateIncome(self, ampl):
		sold = np.array(ampl.getVariable('SPRZEDAZ').getValues().toPandas().as_matrix())
		price = np.array(ampl.getParameter('CENA').getValues().toPandas().as_matrix())
		income_per_city = np.multiply(sold, price)

		return np.transpose(income_per_city)

	def calculateTotalIncome(self, income):
		totalIncome = np.sum(income)
		return totalIncome

	def calculateCapacityUsed(self, capacity, sales):
		salesTotal = 0
		for inCitySales in sales:
			salesTotal += np.sum(inCitySales)
		capacityUsed = (salesTotal / capacity) * 100
		return capacityUsed

	def collectResult(self, id, ampl, cities):
		num_of_cities = len(cities)

		cargo = self.get_np_array_from_variable(ampl, 'ZABRANE')
		sales = self.get_np_array_from_variable(ampl, 'SPRZEDAZ', 
			True, (num_of_cities, -1))
		road = self.get_np_array_from_variable(ampl, 'UZYCIE_DROGI', 
			True, (num_of_cities, num_of_cities))
		path = self.findPathInRoad(cities, road)
		income = self.calculateIncome(ampl).reshape(num_of_cities, -1)
		totalIncome = self.calculateTotalIncome(income)
		capacityUsed = self.calculateCapacityUsed(self.data.capacity[id], sales)
		result = Model.Result(id, cargo, sales, road, path, income, totalIncome, capacityUsed);
		return result

	def get_np_array_from_variable(self, ampl, name, two_dim=False, shape=(-1, 1)):
		tmp = np.transpose(ampl.getVariable(name).getValues().toPandas().as_matrix())
		if two_dim:
			tmp = np.reshape(tmp, shape)
		return tmp

	class Struct(object): pass

	def load_data(self, data_dir):

		# Load numerical data
		data = Model.Struct()
		data.demand = np.genfromtxt('{0}/demand'.format(data_dir), delimiter=",")
		data.supply = np.genfromtxt('{0}/supply'.format(data_dir), delimiter=",")
		data.prices = np.genfromtxt('{0}/prices'.format(data_dir), delimiter=",")
		data.roads = np.genfromtxt('{0}/roads'.format(data_dir), delimiter=",")
		data.shortage_coeff = np.genfromtxt('{0}/shortage_coeff'.format(data_dir), delimiter=",")
		data.capacity = np.genfromtxt('{0}/capacity'.format(data_dir), delimiter=",")
		data.volumes = np.genfromtxt('{0}/volumes'.format(data_dir), delimiter=",")
		data.coordinates = np.genfromtxt('{0}/coordinates'.format(data_dir), delimiter=",")
		# Load textual data
		data.cities = np.array([line.rstrip('\n') for line in open('{0}/cities'.format(data_dir))])
		data.breadTypes = np.array([line.rstrip('\n') for line in open('{0}/types'.format(data_dir))])
		data.citiesTotal = len(data.cities)
		data.carsTotal = len(data.capacity)
		return data

	# Calculates simplified demand as total volume of products needed to fulfill
	# the demand
	def get_simplified_demand(self, demand, volumes):

		simplified_demand = np.zeros((demand.shape[0], 1))

		for idx0, row in enumerate(demand):
			overall_volume = 0
			for idx1, elem in enumerate(row):
				overall_volume += elem * volumes[idx1]
			simplified_demand[idx0] = overall_volume

		return simplified_demand

	def run_sweep(self, data):

	    # Calculate simplified demand
	    simplified_demand = self.get_simplified_demand(data.demand, data.volumes)

	    # Get bakery coefficients
	    depot_coordinates = (data.coordinates[0,0], data.coordinates[0,1])

	    points = np.append(data.coordinates[1:, :], simplified_demand[1:], axis=1)
	    (points, order, cars_used) = sweep(points, data.capacity, depot_coordinates)

	    result = []
	    for car_id in range(0, cars_used):

	        # Generate list od cities/points belonging to this cluster
	        cities = []
	        for index, (_,_,_,_,id) in enumerate(points):
	            if car_id == id:
	                cities.append(index)

	        # Get original IDs (before sorting)
	        cities = order[cities]

	        # Increase IDs by one and add bakery (it was removed earlier before
	        #running SWEEP). Then sort indices
	        cities = np.sort(np.append(0, np.add(cities, 1)))

	        result.append((car_id, cities))

	    return result

	def run_clarke_wright(self, data):

	    # Calculate simplified demand
	    simplified_demand = self.get_simplified_demand(data.demand, data.volumes)

	    capacity = data.capacity
	    #if len(data.capacity) != 1:
	    #    print("Warning: Clarke Wright algorithm assumes equal capacities of all cars")
	    #    capacity = data.capacity[0]

	    result = clarke_wright(data.roads, simplified_demand, capacity)

	    print('Result:\n')
	    print(result)

	    return result

	def get_data_subset(self, data, car_id, city_ids):

		data_subset = deepcopy(data)

		tmp = data_subset.roads[city_ids,:]
		data_subset.roads = tmp[:,city_ids]

		data_subset.cities = data_subset.cities[city_ids]
		data_subset.demand = data_subset.demand[city_ids]
		data_subset.prices = data_subset.prices[city_ids]
		data_subset.shortage_coeff = data_subset.shortage_coeff[city_ids]
		data_subset.capacity = data_subset.capacity[car_id]
		data_subset.coordinates = data_subset.coordinates[city_ids]

		return data_subset