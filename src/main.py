import sys
from PyQt5.QtWidgets import QApplication, QDialog

from src.view.root_window import RootWindow


class MainDialog(QDialog):
    main_ui = None

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.main_ui = RootWindow()
        self.main_ui.setup_ui(self)


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.show()
    sys.exit(myapp.exec_())
