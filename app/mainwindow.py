from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from ui.ui_mainwindow import Ui_MainWindow
from resultsdialog import ResultsDialog
import rc.images_rc

from model.model import Model

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		# Set up the user interface from Designer.
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.loadDataDialog = QFileDialog()
		self.loadDataDialog.setFileMode(QFileDialog.DirectoryOnly)
		self.loadDataDialog.setOption(QFileDialog.ShowDirsOnly, True)
		self.loadDataDialog.setAcceptMode(QFileDialog.AcceptOpen)
		self.loadDataDialog.fileSelected.connect(self.directorySelected)

		self.ui.loadDataButton.clicked.connect(self.loadDataDialog.show)
		self.ui.calculateButton.clicked.connect(self.calculateClicked)

	@pyqtSlot(str)
	def directorySelected(self, dataDirectory):
		print("Selected data directory: {0}".format(dataDirectory))
		self.loadData(dataDirectory)

	def loadData(self, dataDirectory):
		print("Loading model with data from: {0}".format(dataDirectory))
		self.ui.loadDataButton.setEnabled(False)
		self.ui.statusLabel.setText("Loading model, please wait...")

		try:
			self.model = Model(dataDirectory)
		except Exception as ex:
			print("Model load error: {0}".format(ex))
			self.ui.statusLabel.setText("Error occured during loading the model. Please, try again.")
			self.ui.statusLabel.setStyleSheet("color: red")
			self.ui.loadDataButton.setEnabled(True)
			return

		self.ui.statusLabel.setStyleSheet("color: orange")
		self.ui.statusLabel.setText("Model loaded sucessfully. Now you can start calculations.")
		self.ui.loadDataButton.setEnabled(True)
		self.ui.calculateButton.setEnabled(True)

		print("Model loaded successfully")

	@pyqtSlot()
	def calculateClicked(self):
		print("Running model")

		self.ui.loadDataButton.setEnabled(False)
		self.ui.calculateButton.setEnabled(False)
		self.ui.statusLabel.setText("Running model, please wait...")

		try:
			carsUsage = self.model.run()
		except Exception as ex:
			print("Model run error: {0}".format(ex))
			self.ui.statusLabel.setText("Error occured during running the model. Please, try again.")
			self.ui.statusLabel.setStyleSheet("color: red")
			self.ui.loadDataButton.setEnabled(True)
			return

		self.ui.statusLabel.setText("Model calculated successfully!")
		self.ui.statusLabel.setStyleSheet("color: green")

		self.openResultsDialog(carsUsage)

	def openResultsDialog(self, results):
		print("Opening results dialog")

		self.resultsDialog = ResultsDialog(self.model.breadTypes, self.model.cities, results)
		self.resultsDialog.finished.connect(self.resultsDialogFinished)
		self.resultsDialog.setModal(True)
		self.resultsDialog.show()

		print("Results dialog opened")

	@pyqtSlot()
	def resultsDialogFinished(self):
		self.ui.statusLabel.setText("Please load new data for model.")
		self.ui.statusLabel.setStyleSheet("");
		self.ui.loadDataButton.setEnabled(True)

