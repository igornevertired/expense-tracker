from src.ui import FinanceDashboard
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceDashboard()
    window.show()
    sys.exit(app.exec())
