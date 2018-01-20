from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from ui.ui_mainwindow import Ui_MainWindow
from resultsdialog import ResultsDialog
from aboutdialog import AboutDialog
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
		self.ui.actionAbout.triggered.connect(self.actionAboutTriggered)

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

		self.triggerModelLoaded()

		print("Model loaded successfully")

	def triggerModelLoaded(self):
		self.ui.statusLabel.setStyleSheet("color: orange")
		self.ui.statusLabel.setText("Model loaded sucessfully. Now you can start calculations.")
		self.ui.loadDataButton.setEnabled(True)
		self.ui.calculateButton.setEnabled(True)

	@pyqtSlot()
	def calculateClicked(self):
		print("Running model")

		if self.ui.useSweepRadioButton.isChecked():
			algorithmType = Model.AlgorithmType.Sweep
		elif self.ui.useClarkeWrightRadioButton.isChecked():
			algorithmType = Model.AlgorithmType.ClarkeWright
		else:
			assert False, "Either Sweep or ClarkeWright should be checked"

		self.ui.loadDataButton.setEnabled(False)
		self.ui.calculateButton.setEnabled(False)
		self.ui.useSweepRadioButton.setEnabled(False)
		self.ui.useClarkeWrightRadioButton.setEnabled(False)
		self.ui.statusLabel.setText("Running model, please wait...")

		try:
			carsUsage, _ = self.model.run(algorithmType)
		except Exception as ex:
			print("Model run error: {0}".format(ex))
			self.ui.statusLabel.setText("Error occured during running the model. Please, try again.")
			self.ui.statusLabel.setStyleSheet("color: red")
			self.ui.loadDataButton.setEnabled(True)
			self.ui.useSweepRadioButton.setEnabled(True)
			self.ui.useClarkeWrightRadioButton.setEnabled(True)
			raise

		self.ui.statusLabel.setText("Model calculated successfully!")
		self.ui.statusLabel.setStyleSheet("color: green")

		self.openResultsDialog(carsUsage)

	def openResultsDialog(self, modelResults):
		print("Opening results dialog")

		self.resultsDialog = ResultsDialog(self.model.data, modelResults, self)
		self.resultsDialog.finished.connect(self.resultsDialogFinished)
		self.resultsDialog.setModal(True)
		self.resultsDialog.show()

		print("Results dialog opened")

	@pyqtSlot()
	def resultsDialogFinished(self):
		self.triggerModelLoaded()
		self.ui.useSweepRadioButton.setEnabled(True)
		self.ui.useClarkeWrightRadioButton.setEnabled(True)

	@pyqtSlot()
	def actionAboutTriggered(self):
		self.aboutDialog = AboutDialog(self)
		self.aboutDialog.show()