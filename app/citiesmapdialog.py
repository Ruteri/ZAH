from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QLabel
from ui.ui_citiesmapdialog import Ui_CitiesMapDialog
from citiesmapwidget import CitiesMapWidget

class CitiesMapDialog(QDialog):
	def __init__(self, coordinates, paths, parent):
		super(CitiesMapDialog, self).__init__(parent)

		# Set up the user interface from Designer.
		self.ui = Ui_CitiesMapDialog()
		self.ui.setupUi(self)

		print("Coordinates: {0}".format(coordinates))
		print("Paths: {0}".format(paths))

		self.ui.citiesMapWidget = CitiesMapWidget(coordinates, paths, self)
		self.ui.gridLayout.addWidget(self.ui.citiesMapWidget, 5, 0, 1, 4)

		self.ui.carIdComboBox.activated.connect(self.carIdActivated)

		self.loadCarsIds(paths)

	def loadCarsIds(self, paths):
		carId = 0
		for path in paths:
			self.ui.carIdComboBox.addItem(str(carId), path)
			carId += 1

		self.carIdActivated(0)

	@pyqtSlot(int)
	def carIdActivated(self, index):
		print("carIdActivated index={0}".format(index))
		path = self.ui.carIdComboBox.itemData(index)
		print("carIdActivated path={0}".format(path))
		self.ui.citiesMapWidget.setCurrentPath(path)


