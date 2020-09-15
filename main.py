import sys

from PyQt5.QtWidgets import QApplication, QDialog

from src.utils.logger_utils import init_log, lg
from src.view.root_window import RootWindow


class MainDialog(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.main_ui = RootWindow()
        self.main_ui.setup_ui(self)


if __name__ == '__main__':
    try:
        init_log()
        myapp = QApplication(sys.argv)
        myDlg = MainDialog()
        myDlg.show()
        sys.exit(myapp.exec_())
    except Exception as err:
        lg.error(err)