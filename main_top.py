import sys
from PySide6 import QtWidgets

from src.MainWindow import MainUI

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainUI()
    main.showMaximized()
    sys.exit(app.exec())
