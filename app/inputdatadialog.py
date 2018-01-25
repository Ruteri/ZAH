from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from ui.ui_inputdatadialog import Ui_InputDataDialog
import rc.images_rc

class InputDataDialog(QDialog):
	def __init__(self, modelData, parent):
		super(InputDataDialog, self).__init__(parent)

		# Set up the user interface from Designer.
		self.ui = Ui_InputDataDialog()
		self.ui.setupUi(self)

		self.loadModelData(modelData)

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
