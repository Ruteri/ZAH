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

		self.loadModelResults(modelData, modelResults)

		self.ui.carIdComboBox.activated.connect(self.carIdActivated)
		self.ui.showPathPushButton.clicked.connect(self.showPathClicked)

		self.carIdActivated(0)

	def loadModelResults(self, modelData, modelResults):
		print("Model results: {0}".format(modelResults))

		self.loadCarsIds(modelResults)
		self.initCargoPerBreadType(modelData.breadTypes)
		self.initSalesInCities(modelData.breadTypes, modelData.cities)
		self.initIncomeInCities(modelData.breadTypes, modelData.cities)

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

	@pyqtSlot()
	def showPathClicked(self):
		self.citiesMapDialog = CitiesMapDialog(self.coordinates, self.paths, self)
		self.citiesMapDialog.setModal(True)
		self.citiesMapDialog.show()
