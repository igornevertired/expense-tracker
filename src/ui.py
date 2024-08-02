import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QDialog, QLabel, QLineEdit, QDateTimeEdit, QFormLayout
from PyQt6.QtCore import Qt, QDateTime
from src.database import get_transactions, add_transaction


class AddTransactionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Transaction")
        self.setFixedSize(300, 200)

        layout = QFormLayout()

        self.amount_input = QLineEdit(self)
        self.category_input = QLineEdit(self)
        self.date_input = QDateTimeEdit(self)
        self.date_input.setDateTime(QDateTime.currentDateTime())
        self.description_input = QLineEdit(self)

        layout.addRow(QLabel("Amount:"), self.amount_input)
        layout.addRow(QLabel("Category:"), self.category_input)
        layout.addRow(QLabel("Date:"), self.date_input)
        layout.addRow(QLabel("Description:"), self.description_input)

        self.add_button = QPushButton("Add", self)
        self.add_button.clicked.connect(self.add_transaction)
        layout.addRow(self.add_button)

        self.setLayout(layout)

    def add_transaction(self):
        amount = float(self.amount_input.text())
        category = self.category_input.text()
        date = self.date_input.dateTime().toPyDateTime()
        description = self.description_input.text()

        add_transaction(amount, category, date, description)
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transaction Manager")
        self.setGeometry(100, 100, 800, 600)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Amount", "Category", "Date", "Description"])

        self.add_button = QPushButton("Add Transaction", self)
        self.add_button.clicked.connect(self.show_add_dialog)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.add_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.refresh_table()

    def show_add_dialog(self):
        dialog = AddTransactionDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_table()

    def refresh_table(self):
        transactions = get_transactions()
        self.table.setRowCount(len(transactions))

        for row, transaction in enumerate(transactions):
            self.table.setItem(row, 0, QTableWidgetItem(str(transaction.amount)))
            self.table.setItem(row, 1, QTableWidgetItem(transaction.category))
            self.table.setItem(row, 2, QTableWidgetItem(transaction.date.strftime('%Y-%m-%d %H:%M:%S')))
            self.table.setItem(row, 3, QTableWidgetItem(transaction.description))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
