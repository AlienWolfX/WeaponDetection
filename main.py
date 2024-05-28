from PyQt5.QtWidgets import QApplication
import sys
from GuardianEye import GuardianEye

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GuardianEye()
    ex.show()
    sys.exit(app.exec_())