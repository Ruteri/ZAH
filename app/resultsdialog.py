from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from ui.ui_resultsdialog import Ui_ResultsDialog
from citiesmapdialog import CitiesMapDialog
import rc.images_rc
from collections import namedtuple

class ResultsDialog(QDialog):
	def __init__(self, modelData, modelResults, parent):
		super(ResultsDialog, self).__init__(parent)

		# Set up the user interface from Designer.
		self.ui = Ui_ResultsDialog()
		self.ui.setupUi(self)

		self.coordinates = modelData.coordinates
		self.paths = [modelResult.path for modelResult in modelResults]

		self.loadModelData(modelData)
		self.loadModelResults(modelData, modelResults)

		self.ui.carIdComboBox.activated.connect(self.carIdActivated)
		self.ui.showPathPushButton.clicked.connect(self.showPathClicked)

		self.carIdActivated(0)

	def loadModelData(self, modelData):
		print("Model data: {0}".format(modelData))

		self.ui.citiesTotalLabel.setText(str(modelData.citiesTotal))
		self.ui.carsTotalLabel.setText(str(modelData.carsTotal))
		self.ui.breadTypesTotalLabel.setText(str(len(modelData.breadTypes)))

		self.loadTotalDemandPerBreadTypes(modelData.breadTypes, modelData.demand)
		self.loadVolumesOfBreadTypes(modelData.breadTypes, modelData.volumes)
		self.loadCarsCapacities(modelData.capacity)
		self.loadDemandInCities(modelData.breadTypes, modelData.demand)
		self.loadPricesInCities(modelData.breadTypes, modelData.prices)

	def loadModelResults(self, modelData, modelResults):
		print("Model results: {0}".format(modelResults))

		self.loadCarsIds(modelResults)
		self.initCargoPerBreadType(modelData.breadTypes)
		self.initSalesInCities(modelData.breadTypes, modelData.cities)
		self.initIncomeInCities(modelData.breadTypes, modelData.cities)

	def loadTotalDemandPerBreadTypes(self, breadTypes, demand):
		horizontalHeaderLabels = ["Bread type", "Total demand"]
		self.ui.totalDemandPerBreadTypesTableWidget.setColumnCount(len(horizontalHeaderLabels))
		self.ui.totalDemandPerBreadTypesTableWidget.setHorizontalHeaderLabels(horizontalHeaderLabels)
		self.ui.totalDemandPerBreadTypesTableWidget.setRowCount(len(breadTypes))
		for rowIndex in range(len(breadTypes)):
			breadType = breadTypes[rowIndex]
			breadTypeItem = QTableWidgetItem(breadType)
			self.ui.totalDemandPerBreadTypesTableWidget.setItem(rowIndex, 0,
				breadTypeItem)

			totalDemandPerBreadType = 0
			for demandInCityPerBreadType in demand:
				totalDemandPerBreadType += demandInCityPerBreadType[rowIndex]
			totalDemandPerBreadTypeItem = QTableWidgetItem(str(totalDemandPerBreadType))
			self.ui.totalDemandPerBreadTypesTableWidget.setItem(rowIndex, 1,
				totalDemandPerBreadTypeItem)

			# supplyPerBreadType = supply[rowIndex]
			# supplyPerBreadTypeItem = QTableWidgetItem(str(supplyPerBreadType))
			# self.ui.totalDemandPerBreadTypesTableWidget.setItem(rowIndex, 1,
			# 	supplyPerBreadTypeItem)

	def loadVolumesOfBreadTypes(self, breadTypes, volumes):
		print("Volumes: {0}".format(volumes))
		horizontalHeaderLabels = ["Bread type", "Volume"]
		self.ui.volumesOfBreadTypesTableWidget.setColumnCount(len(horizontalHeaderLabels))
		self.ui.volumesOfBreadTypesTableWidget.setHorizontalHeaderLabels(horizontalHeaderLabels)
		self.ui.volumesOfBreadTypesTableWidget.setRowCount(len(breadTypes))
		for rowIndex in range(len(breadTypes)):
			breadType = breadTypes[rowIndex]
			breadTypeItem = QTableWidgetItem(breadType)
			self.ui.volumesOfBreadTypesTableWidget.setItem(rowIndex, 0,
				breadTypeItem)

			volumeOfBreadType = volumes[rowIndex]
			volumeOfBreadTypeItem = QTableWidgetItem(str(volumeOfBreadType))
			self.ui.volumesOfBreadTypesTableWidget.setItem(rowIndex, 1,
				volumeOfBreadTypeItem)

	def loadCarsCapacities(self, capacities):
		print("Capacities: {0}".format(capacities))
		horizontalHeaderLabels = ["Car ID", "Capacity"]
		self.ui.carsCapacitiesTableWidget.setHorizontalHeaderLabels(horizontalHeaderLabels)
		self.ui.carsCapacitiesTableWidget.setColumnCount(len(horizontalHeaderLabels))
		self.ui.carsCapacitiesTableWidget.setRowCount(len(capacities))
		for rowIndex in range(len(capacities)):
			carId = rowIndex
			carIdItem = QTableWidgetItem(str(carId))
			self.ui.carsCapacitiesTableWidget.setItem(rowIndex, 0,
				carIdItem)

			carCapacity = capacities[rowIndex]
			carCapacityItem = QTableWidgetItem(str(carCapacity))
			self.ui.carsCapacitiesTableWidget.setItem(rowIndex, 1,
				carCapacityItem)

	def loadDemandInCities(self, breadTypes, demand):
		print("Demand: {0}".format(demand))
		print("Demand len: {0}".format(len(demand)))

		cityIds = [("City " + str(i)) for i in range(len(demand))]
		horizontalHeaderLabels = ["Bread type"] + cityIds
		print("horizontalHeaderLabels: {0}".format(horizontalHeaderLabels))
		self.ui.demandInCitiesTableWidget.setColumnCount(len(horizontalHeaderLabels))
		self.ui.demandInCitiesTableWidget.setRowCount(len(breadTypes))
		self.ui.demandInCitiesTableWidget.setHorizontalHeaderLabels(horizontalHeaderLabels)
		for rowIndex in range(len(breadTypes)):
			breadType = breadTypes[rowIndex]
			breadTypeItem = QTableWidgetItem(breadType)
			self.ui.demandInCitiesTableWidget.setItem(rowIndex, 0,
				breadTypeItem)			

			for colIndex in range(len(demand)):
				demandInCity = demand[colIndex, rowIndex]
				demandInCityItem = QTableWidgetItem(str(demandInCity))
				self.ui.demandInCitiesTableWidget.setItem(rowIndex, colIndex + 1,
					demandInCityItem)

	def loadPricesInCities(self, breadTypes, prices):
		print("prices: {0}".format(prices))
		print("Prices len: {0}".format(len(prices)))

		cityIds = [("City " + str(i)) for i in range(len(prices))]
		horizontalHeaderLabels = ["Bread type"] + cityIds
		print("horizontalHeaderLabels: {0}".format(horizontalHeaderLabels))
		self.ui.pricesInCitiesTableWidget.setColumnCount(len(horizontalHeaderLabels))
		self.ui.pricesInCitiesTableWidget.setRowCount(len(breadTypes))
		self.ui.pricesInCitiesTableWidget.setHorizontalHeaderLabels(horizontalHeaderLabels)
		for rowIndex in range(len(breadTypes)):
			breadType = breadTypes[rowIndex]
			breadTypeItem = QTableWidgetItem(breadType)
			self.ui.pricesInCitiesTableWidget.setItem(rowIndex, 0,
				breadTypeItem)			

			for colIndex in range(len(prices)):
				pricesInCity = prices[colIndex, rowIndex]
				pricesInCityItem = QTableWidgetItem(str(pricesInCity))
				self.ui.pricesInCitiesTableWidget.setItem(rowIndex, colIndex + 1,
					pricesInCityItem)

	def loadCarsIds(self, modelResults):
		print("modelResults: {0}".format(modelResults))

		for i in range(len(modelResults)):
			carIdText = "Car " + str(i)
			modelResult = modelResults[i]
			self.ui.carIdComboBox.addItem(carIdText, modelResult)

	def initCargoPerBreadType(self, breadTypes):
		print("breadTypes: {0}".format(breadTypes))
		horizontalHeaderLabels = ["Bread type", "Cargo"]
		self.ui.cargoPerBreadTypeTableWidget.setColumnCount(len(horizontalHeaderLabels))
		self.ui.cargoPerBreadTypeTableWidget.setRowCount(len(breadTypes))
		self.ui.cargoPerBreadTypeTableWidget.setHorizontalHeaderLabels(horizontalHeaderLabels)
		for rowIndex in range(len(breadTypes)):
			breadType = breadTypes[rowIndex]
			breadTypeItem = QTableWidgetItem(breadType)
			self.ui.cargoPerBreadTypeTableWidget.setItem(rowIndex, 0,
				breadTypeItem)

	def initSalesInCities(self, breadTypes, cities):
		print("breadTypes: {0}".format(breadTypes))
		cityIds = [("City " + str(i)) for i in range(len(cities))]
		horizontalHeaderLabels = ["Bread type"] + cityIds
		self.ui.salesInCitiesTableWidget.setColumnCount(len(horizontalHeaderLabels))
		self.ui.salesInCitiesTableWidget.setRowCount(len(breadTypes))
		self.ui.salesInCitiesTableWidget.setHorizontalHeaderLabels(horizontalHeaderLabels)
		for rowIndex in range(len(breadTypes)):
			breadType = breadTypes[rowIndex]
			breadTypeItem = QTableWidgetItem(breadType)
			self.ui.salesInCitiesTableWidget.setItem(rowIndex, 0,
				breadTypeItem)

	def initIncomeInCities(self, breadTypes, cities):
		print("breadTypes: {0}".format(breadTypes))
		cityIds = [("City " + str(i)) for i in range(len(cities))]
		horizontalHeaderLabels = ["Bread type"] + cityIds
		self.ui.incomeInCitiesTableWidget.setColumnCount(len(horizontalHeaderLabels))
		self.ui.incomeInCitiesTableWidget.setRowCount(len(breadTypes))
		self.ui.incomeInCitiesTableWidget.setHorizontalHeaderLabels(horizontalHeaderLabels)
		for rowIndex in range(len(breadTypes)):
			breadType = breadTypes[rowIndex]
			breadTypeItem = QTableWidgetItem(breadType)
			self.ui.incomeInCitiesTableWidget.setItem(rowIndex, 0,
				breadTypeItem)

	@pyqtSlot(int)
	def carIdActivated(self, index):
		print("carIdActivated index={0}".index)

		modelResult = self.ui.carIdComboBox.itemData(index)
		self.ui.capacityUsedLabel.setText(str(modelResult.capacityUsed) + "%")
		self.ui.totalIncomeLabel.setText(str(modelResult.totalIncome))

		self.updateCargoPerBreadType(modelResult.cargo)
		self.updateSalesInCities(modelResult.path, modelResult.sales)
		self.updateIncomeInCities(modelResult.path, modelResult.income)

	def updateCargoPerBreadType(self, cargo):
		print("Cargo: {0}".format(cargo))
		rowCount = self.ui.cargoPerBreadTypeTableWidget.rowCount()
		print("Row count: {0}".format(rowCount))
		for rowIndex in range(rowCount):
			cargoPerBread = cargo[0, rowIndex]
			cargoPerBreadItem = QTableWidgetItem(str(cargoPerBread))
			self.ui.cargoPerBreadTypeTableWidget.setItem(rowIndex, 1,
				cargoPerBreadItem)

	def updateSalesInCities(self, path, sales):
		assert len(path) == len(sales), "Length of path and sales must be the same"
		rowCount = self.ui.salesInCitiesTableWidget.rowCount()
		for i in range(len(path)):
			cityId = path[i]
			colIndex = cityId
			salesInCityPerBreadTypes = sales[i]
			assert rowCount == len(salesInCityPerBreadTypes), "sales in city per bread type must have rowCount elements"
			for rowIndex in range(rowCount):
				salesInCityPerBreadType = salesInCityPerBreadTypes[rowIndex]
				salesInCityPerBreadTypeItem = QTableWidgetItem(str(salesInCityPerBreadType))
				self.ui.salesInCitiesTableWidget.setItem(rowIndex, colIndex+1,
					salesInCityPerBreadTypeItem)

	def updateIncomeInCities(self, path, income):
		print("len income: {0}".format(len(income)))
		print("len path: {0}".format(len(path)))
		assert len(path) == len(income), "Length of path and income must be the same"
		rowCount = self.ui.incomeInCitiesTableWidget.rowCount()
		print("rowCount: {0}".format(rowCount))
		for i in range(len(path)):
			cityId = path[i]
			colIndex = cityId
			incomeInCityPerBreadTypes = income[i]
			print("incomeInCityPerBreadTypes: {0}".format(incomeInCityPerBreadTypes))
			assert rowCount == len(incomeInCityPerBreadTypes), "income in city per bread type must have rowCount elements"
			for rowIndex in range(rowCount):
				incomeInCityPerBreadType = incomeInCityPerBreadTypes[rowIndex]
				incomeInCityPerBreadTypeItem = QTableWidgetItem(str(incomeInCityPerBreadType))
				self.ui.incomeInCitiesTableWidget.setItem(rowIndex, colIndex+1,
					incomeInCityPerBreadTypeItem)

		# print("Bread types: {0}".format(breadTypes))
		# print("Cities: {0}".format(cities))
		# self.breadTypes = breadTypes
		# self.cities = cities
		# self.coordinates = coordinates


		# self.ui.carIdComboBox.activated.connect(self.carIdActivated)
		# self.ui.cityIdComboBox.activated.connect(self.cityIdActivated)
		# self.ui.showPathPushButton.clicked.connect(self.showPathClicked)

		# self.setupCargoTableWidget()
		# self.setupDetailsTableWidget()
		# self.loadCarsUsage(carsUsage)

	# def setupCargoTableWidget(self):
	# 	cargoLabels = ["Cargo (per bread type)"]
	# 	self.ui.cargoTableWidget.setColumnCount(len(self.breadTypes))
	# 	self.ui.cargoTableWidget.setRowCount(len(cargoLabels))
	# 	self.ui.cargoTableWidget.setHorizontalHeaderLabels(self.breadTypes)
	# 	self.ui.cargoTableWidget.setVerticalHeaderLabels(cargoLabels)

	# def setupDetailsTableWidget(self):
	# 	detailsLabels = ["Sales (per bread type)", "Income (per bread type)"]
	# 	self.ui.detailsTableWidget.setColumnCount(len(self.breadTypes))
	# 	self.ui.detailsTableWidget.setHorizontalHeaderLabels(self.breadTypes)
	# 	self.ui.detailsTableWidget.setRowCount(len(detailsLabels))
	# 	self.ui.detailsTableWidget.setVerticalHeaderLabels(detailsLabels)

	# def loadCarsUsage(self, carsUsage):
	# 	for carUsage in carsUsage:
	# 		carId = carUsage.carId
	# 		self.ui.carIdComboBox.addItem(str(carId), carUsage)

	# 	self.carIdActivated(0)

	# @pyqtSlot(int)
	# def carIdActivated(self, index):
	# 	print("New car index: {0}".format(index))

	# 	carUsage = self.ui.carIdComboBox.itemData(index)
	# 	print("Car usage: {0}".format(carUsage))

	# 	self.ui.carIdLabel.setText(str(carUsage.carId))
	# 	self.ui.totalIncomeLabel.setText(str(carUsage.totalIncome))

	# 	for x in range(len(self.breadTypes)):
	# 		cargoItemText = str(carUsage.cargo[0, x])
	# 		cargoItem = QTableWidgetItem(cargoItemText)
	# 		self.ui.cargoTableWidget.setItem(0, x, cargoItem)

	# 	self.loadCarUsageDetails(carUsage)

	# def loadCarUsageDetails(self, carUsage):
	# 	self.ui.cityIdComboBox.clear();
	# 	cityId = 0
	# 	[citiesCount, _] = carUsage.sales.shape;
	# 	for cityIndex in range(citiesCount):
	# 		salesPerCity = carUsage.sales[cityIndex,]
	# 		incomePerCity = carUsage.income[cityIndex,]
	# 		carUsageDetails = CarUsageDetails(salesPerCity, incomePerCity)
	# 		# cityId = self.cities[cityIndex]
	# 		self.ui.cityIdComboBox.addItem(str(cityId), carUsageDetails)
	# 		cityId += 1

	# 	self.cityIdActivated(0)

	# @pyqtSlot(int)
	# def cityIdActivated(self, index):
	# 	print("New city index: {0}".format(index))

	# 	carUsageDetails = self.ui.cityIdComboBox.itemData(index)
	# 	print("Car usage details: {0}".format(carUsageDetails))

	# 	for x in range(len(self.breadTypes)):
	# 		salesItemText = str(carUsageDetails.salesPerCity[x])
	# 		salesItem = QTableWidgetItem(salesItemText)
	# 		self.ui.detailsTableWidget.setItem(0, x, salesItem)

	# 		incomeItemText = str(carUsageDetails.incomePerCity[x])
	# 		incomeItem = QTableWidgetItem(incomeItemText)
	# 		self.ui.detailsTableWidget.setItem(1, x, incomeItem)

	@pyqtSlot()
	def showPathClicked(self):
		self.citiesMapDialog = CitiesMapDialog(self.coordinates, self.paths, self)
		self.citiesMapDialog.setModal(True)
		self.citiesMapDialog.show()
