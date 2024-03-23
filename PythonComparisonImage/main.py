import sys

from PyQt5.QtWidgets import QApplication
import UI.main_app as ui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ui.MainApp()
    window.show()
    sys.exit(app.exec_())


