from PyQt5.QtWidgets import QDialog
from ui.ui_resultsdialog import Ui_ResultsDialog
import rc.images_rc

class ResultsDialog(QDialog):
    def __init__(self, results):
        super(ResultsDialog, self).__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_ResultsDialog()
        self.ui.setupUi(self)
        self.results = results
