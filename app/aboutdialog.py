from PyQt5.QtWidgets import QDialog
from ui.ui_aboutdialog import Ui_AboutDialog

class AboutDialog(QDialog):
	def __init__(self):
		super(AboutDialog, self).__init__()

		# Set up the user interface from Designer.
		self.ui = Ui_AboutDialog()
		self.ui.setupUi(self)