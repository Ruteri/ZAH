from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from ui.ui_resultsdialog import Ui_ResultsDialog
import rc.images_rc
from collections import namedtuple

CarUsageDetails = namedtuple('CarUsageDetails', ['salesPerCity', 'incomePerCity'])

class ResultsDialog(QDialog):
	def __init__(self, breadTypes, cities, carsUsage):
		super(ResultsDialog, self).__init__()

		# Set up the user interface from Designer.
		self.ui = Ui_ResultsDialog()
		self.ui.setupUi(self)

		print("Bread types: {0}".format(breadTypes))
		print("Cities: {0}".format(cities))
		self.breadTypes = breadTypes
		self.cities = cities

		self.ui.carIdComboBox.activated.connect(self.carIdActivated)
		self.ui.cityIdComboBox.activated.connect(self.cityIdActivated)

		self.setupCargoTableWidget()
		self.setupDetailsTableWidget()
		self.loadCarsUsage(carsUsage)

	def setupCargoTableWidget(self):
		cargoLabels = ["Cargo (per bread type)"]
		self.ui.cargoTableWidget.setColumnCount(len(self.breadTypes))
		self.ui.cargoTableWidget.setRowCount(len(cargoLabels))
		self.ui.cargoTableWidget.setHorizontalHeaderLabels(self.breadTypes)
		self.ui.cargoTableWidget.setVerticalHeaderLabels(cargoLabels)

	def setupDetailsTableWidget(self):
		detailsLabels = ["Sales (per bread type)", "Income (per bread type)"]
		self.ui.detailsTableWidget.setColumnCount(len(self.breadTypes))
		self.ui.detailsTableWidget.setHorizontalHeaderLabels(self.breadTypes)
		self.ui.detailsTableWidget.setRowCount(len(detailsLabels))
		self.ui.detailsTableWidget.setVerticalHeaderLabels(detailsLabels)

	def loadCarsUsage(self, carsUsage):
		for carUsage in carsUsage:
			carId = carUsage.carId
			self.ui.carIdComboBox.addItem(str(carId), carUsage)

		self.carIdActivated(0)

	@pyqtSlot(int)
	def carIdActivated(self, index):
		print("New car index: {0}".format(index))

		carUsage = self.ui.carIdComboBox.itemData(index)
		print("Car usage: {0}".format(carUsage))

		self.ui.carIdLabel.setText(str(carUsage.carId))
		self.ui.totalIncomeLabel.setText(str(carUsage.totalIncome))

		for x in range(len(self.breadTypes)):
			cargoItemText = str(carUsage.cargo[0, x])
			cargoItem = QTableWidgetItem(cargoItemText)
			self.ui.cargoTableWidget.setItem(0, x, cargoItem)

		self.loadCarUsageDetails(carUsage)

	def loadCarUsageDetails(self, carUsage):
		self.ui.cityIdComboBox.clear();
		[citiesCount, _] = carUsage.sales.shape;
		for cityIndex in range(citiesCount):
			salesPerCity = carUsage.sales[cityIndex,]
			incomePerCity = carUsage.income[cityIndex,]
			carUsageDetails = CarUsageDetails(salesPerCity, incomePerCity)
			cityId = self.cities[cityIndex]
			self.ui.cityIdComboBox.addItem(cityId, carUsageDetails)

		self.cityIdActivated(0)

	@pyqtSlot(int)
	def cityIdActivated(self, index):
		print("New city index: {0}".format(index))

		carUsageDetails = self.ui.cityIdComboBox.itemData(index)
		print("Car usage details: {0}".format(carUsageDetails))

		for x in range(len(self.breadTypes)):
			salesItemText = str(carUsageDetails.salesPerCity[x])
			salesItem = QTableWidgetItem(salesItemText)
			self.ui.detailsTableWidget.setItem(0, x, salesItem)

			incomeItemText = str(carUsageDetails.incomePerCity[x])
			incomeItem = QTableWidgetItem(incomeItemText)
			self.ui.detailsTableWidget.setItem(1, x, incomeItem)

