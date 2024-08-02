import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, \
    QLineEdit, QTableWidget, QTableWidgetItem, QDateEdit, QHeaderView, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate
from src.database import add_transaction, get_transactions, edit_transaction, delete_transaction
import matplotlib.pyplot as plt


class FinanceDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modern Finance Dashboard")
        self.setGeometry(100, 100, 1000, 700)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main Layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Header
        header_layout = QHBoxLayout()
        header_label = QLabel("Finance Dashboard")
        header_label.setFont(QFont("Arial", 24))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(header_label)
        main_layout.addLayout(header_layout)

        # Transaction Form
        form_layout = QHBoxLayout()

        amount_label = QLabel("Amount:")
        amount_label.setFont(QFont("Arial", 14))
        form_layout.addWidget(amount_label)

        self.amount_input = QLineEdit()
        self.amount_input.setFont(QFont("Arial", 14))
        form_layout.addWidget(self.amount_input)

        category_label = QLabel("Category:")
        category_label.setFont(QFont("Arial", 14))
        form_layout.addWidget(category_label)

        self.category_input = QLineEdit()
        self.category_input.setFont(QFont("Arial", 14))
        form_layout.addWidget(self.category_input)

        date_label = QLabel("Date:")
        date_label.setFont(QFont("Arial", 14))
        form_layout.addWidget(date_label)

        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setFont(QFont("Arial", 14))
        form_layout.addWidget(self.date_input)

        description_label = QLabel("Description:")
        description_label.setFont(QFont("Arial", 14))
        form_layout.addWidget(description_label)

        self.description_input = QLineEdit()
        self.description_input.setFont(QFont("Arial", 14))
        form_layout.addWidget(self.description_input)

        add_button = QPushButton("Add Transaction")
        add_button.setFont(QFont("Arial", 14))
        add_button.clicked.connect(self.add_transaction)
        form_layout.addWidget(add_button)

        edit_button = QPushButton("Edit Transaction")
        edit_button.setFont(QFont("Arial", 14))
        edit_button.clicked.connect(self.edit_transaction)
        form_layout.addWidget(edit_button)

        delete_button = QPushButton("Delete Transaction")
        delete_button.setFont(QFont("Arial", 14))
        delete_button.clicked.connect(self.delete_transaction)
        form_layout.addWidget(delete_button)

        main_layout.addLayout(form_layout)

        # Transaction Table
        table_layout = QVBoxLayout()

        table_label = QLabel("Recent Transactions")
        table_label.setFont(QFont("Arial", 18))
        table_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        table_layout.addWidget(table_label)

        self.transaction_table = QTableWidget(0, 5)
        self.transaction_table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount", "Description"])
        self.transaction_table.horizontalHeader().setFont(QFont("Arial", 14))
        self.transaction_table.verticalHeader().setVisible(False)
        self.transaction_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.transaction_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.transaction_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.transaction_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.transaction_table.cellClicked.connect(self.populate_form)

        self.load_transactions()

        table_layout.addWidget(self.transaction_table)
        main_layout.addLayout(table_layout)

        # Plot Button
        plot_button = QPushButton("Plot Expenses by Category")
        plot_button.setFont(QFont("Arial", 14))
        plot_button.clicked.connect(self.plot_expenses)
        main_layout.addWidget(plot_button)

        # Load styles
        self.load_styles()

    def load_styles(self):
        with open("src/styles/styles.qss", "r") as f:
            self.setStyleSheet(f.read())

    def add_transaction(self):
        amount = float(self.amount_input.text())
        category = self.category_input.text()
        date = self.date_input.date().toPyDate()
        description = self.description_input.text()

        add_transaction(amount, category, date, description)
        self.load_transactions()

    def edit_transaction(self):
        selected_row = self.transaction_table.currentRow()
        if selected_row != -1:
            transaction_id = int(self.transaction_table.item(selected_row, 0).text())
            amount = float(self.amount_input.text())
            category = self.category_input.text()
            date = self.date_input.date().toPyDate()
            description = self.description_input.text()

            edit_transaction(transaction_id, amount, category, date, description)
            self.load_transactions()
        else:
            QMessageBox.warning(self, "Warning", "No transaction selected for editing.")

    def delete_transaction(self):
        selected_row = self.transaction_table.currentRow()
        if selected_row != -1:
            transaction_id = int(self.transaction_table.item(selected_row, 0).text())
            delete_transaction(transaction_id)
            self.load_transactions()
        else:
            QMessageBox.warning(self, "Warning", "No transaction selected for deletion.")

    def load_transactions(self):
        transactions = get_transactions()
        self.transaction_table.setRowCount(0)
        for transaction in transactions:
            row_position = self.transaction_table.rowCount()
            self.transaction_table.insertRow(row_position)
            self.transaction_table.setItem(row_position, 0, QTableWidgetItem(str(transaction.id)))
            self.transaction_table.setItem(row_position, 1, QTableWidgetItem(transaction.date.strftime('%Y-%m-%d')))
            self.transaction_table.setItem(row_position, 2, QTableWidgetItem(transaction.category))
            self.transaction_table.setItem(row_position, 3, QTableWidgetItem(f"{transaction.amount:.2f}"))
            self.transaction_table.setItem(row_position, 4, QTableWidgetItem(transaction.description))

    def populate_form(self, row, column):
        self.amount_input.setText(self.transaction_table.item(row, 3).text())
        self.category_input.setText(self.transaction_table.item(row, 2).text())
        self.date_input.setDate(QDate.fromString(self.transaction_table.item(row, 1).text(), "yyyy-MM-dd"))
        self.description_input.setText(self.transaction_table.item(row, 4).text())

    def plot_expenses(self):
        transactions = get_transactions()
        categories = {}
        for transaction in transactions:
            if transaction.category in categories:
                categories[transaction.category] += transaction.amount
            else:
                categories[transaction.category] = transaction.amount

        plt.figure(figsize=(8, 8))
        plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('Expenses by Category')
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceDashboard()
    window.show()
    sys.exit(app.exec())
