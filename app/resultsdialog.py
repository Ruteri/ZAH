from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from ui.ui_resultsdialog import Ui_ResultsDialog
import rc.images_rc

class ResultsDialog(QDialog):
	def __init__(self, carsUsage):
		super(ResultsDialog, self).__init__()

		# Set up the user interface from Designer.
		self.ui = Ui_ResultsDialog()
		self.ui.setupUi(self)

		self.ui.carIdComboBox.activated.connect(self.carIdActivated)

		self.breadTypes = ["Jasne", "Ciemne", "Prawilne"]

		cargoLabels = ["Cargo (per bread type)"]
		self.ui.cargoTableWidget.setColumnCount(len(self.breadTypes))
		self.ui.cargoTableWidget.setRowCount(len(cargoLabels))
		self.ui.cargoTableWidget.setHorizontalHeaderLabels(self.breadTypes)
		self.ui.cargoTableWidget.setVerticalHeaderLabels(cargoLabels)

		detailsLabels = ["Sales (per bread type)", "Income (per bread type)"]
		self.ui.detailsTableWidget.setColumnCount(len(self.breadTypes))
		self.ui.detailsTableWidget.setHorizontalHeaderLabels(self.breadTypes)
		self.ui.detailsTableWidget.setRowCount(len(detailsLabels))
		self.ui.detailsTableWidget.setVerticalHeaderLabels(detailsLabels)

		self.loadCarsUsage(carsUsage)
		self.carIdActivated(0)

	@pyqtSlot(int)
	def carIdActivated(self, index):
		print("Activated index: {0}".format(index))

		carUsage = self.ui.carIdComboBox.itemData(index)
		print("Car usage at activated: {0}".format(carUsage))

		self.ui.carIdLabel.setText(str(carUsage.carId))
		self.ui.totalIncomeLabel.setText(str(carUsage.totalIncome))

		for x in range(len(self.breadTypes)):
			cargoItemText = str(carUsage.cargo[0, x])
			cargoItem = QTableWidgetItem(cargoItemText)
			self.ui.cargoTableWidget.setItem(0, x, cargoItem)

	def loadCarsUsage(self, carsUsage):
		for carUsage in carsUsage:
			carId = carUsage.carId
			self.ui.carIdComboBox.addItem(str(carId), carUsage)
