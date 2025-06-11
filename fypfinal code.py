import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QFormLayout, QDialog, QComboBox, QDateEdit,
    QSpinBox, QDoubleSpinBox, QTextEdit, QFrame, QGraphicsOpacityEffect, QSizePolicy, QGridLayout
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QDate, QPoint
from PyQt5.QtGui import QFont, QColor, QPixmap, QLinearGradient, QPainter, QBrush, QPalette


# ... [Keep all your existing classes: FinancialRecord, InventoryItem, Customer, FinancialDialog, InventoryDialog, CustomerDialog] ...

class FinancialRecord:
    def __init__(self, date, description, amount, record_type):
        self.date = date  # QDate
        self.description = description
        self.amount = amount
        self.record_type = record_type  # "Income" or "Expense"


class InventoryItem:
    def __init__(self, name, quantity, unit_price, supplier, last_updated):
        self.name = name
        self.quantity = quantity
        self.unit_price = unit_price
        self.supplier = supplier
        self.last_updated = last_updated  # QDate


class Customer:
    def __init__(self, name, contact_number, address, email):
        self.name = name
        self.contact_number = contact_number
        self.address = address
        self.email = email


class FinancialDialog(QDialog):
    def __init__(self, parent=None, record=None):
        super().__init__(parent)
        self.setWindowTitle("Add Financial Transaction" if record is None else "Edit Financial Transaction")
        self.setFixedSize(400, 300)
        self.record = record

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        self.description_edit = QLineEdit()
        self.amount_edit = QDoubleSpinBox()
        self.amount_edit.setRange(0.01, 1_000_000_000)
        self.amount_edit.setDecimals(2)
        self.amount_edit.setSingleStep(0.5)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Income", "Expense"])

        form = QFormLayout()
        form.addRow("Date:", self.date_edit)
        form.addRow("Description:", self.description_edit)
        form.addRow("Amount (PKR):", self.amount_edit)
        form.addRow("Type:", self.type_combo)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        if record:
            self.date_edit.setDate(record.date)
            self.description_edit.setText(record.description)
            self.amount_edit.setValue(record.amount)
            self.type_combo.setCurrentText(record.record_type)

    def get_data(self):
        description = self.description_edit.text().strip()
        if not description:
            QMessageBox.warning(self, "Validation Error", "Please enter a description.")
            return None

        amount = self.amount_edit.value()
        if amount <= 0:
            QMessageBox.warning(self, "Validation Error", "Amount must be greater than zero.")
            return None

        return FinancialRecord(
            date=self.date_edit.date(),
            description=description,
            amount=amount,
            record_type=self.type_combo.currentText()
        )


class InventoryDialog(QDialog):
    def __init__(self, parent=None, item=None):
        super().__init__(parent)
        self.setWindowTitle("Add Inventory Item" if item is None else "Edit Inventory Item")
        self.setFixedSize(400, 350)
        self.item = item

        self.name_edit = QLineEdit()
        self.quantity_edit = QSpinBox()
        self.quantity_edit.setRange(0, 1_000_000)
        self.unit_price_edit = QDoubleSpinBox()
        self.unit_price_edit.setRange(0, 1_000_000_000)
        self.unit_price_edit.setDecimals(2)
        self.unit_price_edit.setSingleStep(0.5)
        self.supplier_edit = QLineEdit()
        self.last_updated_edit = QDateEdit()
        self.last_updated_edit.setCalendarPopup(True)
        self.last_updated_edit.setDate(QDate.currentDate())

        form = QFormLayout()
        form.addRow("Product Name:", self.name_edit)
        form.addRow("Quantity:", self.quantity_edit)
        form.addRow("Unit Price (PKR):", self.unit_price_edit)
        form.addRow("Supplier:", self.supplier_edit)
        form.addRow("Last Updated:", self.last_updated_edit)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        if item:
            self.name_edit.setText(item.name)
            self.quantity_edit.setValue(item.quantity)
            self.unit_price_edit.setValue(item.unit_price)
            self.supplier_edit.setText(item.supplier)
            self.last_updated_edit.setDate(item.last_updated)

    def get_data(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation Error", "Please enter product name.")
            return None
        quantity = self.quantity_edit.value()
        unit_price = self.unit_price_edit.value()
        supplier = self.supplier_edit.text().strip()
        last_updated = self.last_updated_edit.date()

        return InventoryItem(name, quantity, unit_price, supplier, last_updated)


class CustomerDialog(QDialog):
    def __init__(self, parent=None, customer=None):
        super().__init__(parent)
        self.setWindowTitle("Add Customer" if customer is None else "Edit Customer")
        self.setFixedSize(450, 400)
        self.customer = customer

        self.name_edit = QLineEdit()
        self.contact_edit = QLineEdit()
        self.address_edit = QTextEdit()
        self.email_edit = QLineEdit()

        form = QFormLayout()
        form.addRow("Customer Name:", self.name_edit)
        form.addRow("Contact Number:", self.contact_edit)
        form.addRow("Address:", self.address_edit)
        form.addRow("Email:", self.email_edit)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        if customer:
            self.name_edit.setText(customer.name)
            self.contact_edit.setText(customer.contact_number)
            self.address_edit.setPlainText(customer.address)
            self.email_edit.setText(customer.email)

    def get_data(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation Error", "Please enter customer name.")
            return None
        contact = self.contact_edit.text().strip()
        if not contact:
            QMessageBox.warning(self, "Validation Error", "Please enter contact number.")
            return None
        address = self.address_edit.toPlainText().strip()
        if not address:
            QMessageBox.warning(self, "Validation Error", "Please enter address.")
            return None
        email = self.email_edit.text().strip()
        if email and ("@" not in email or "." not in email):
            QMessageBox.warning(self, "Validation Error", "Invalid email format.")
            return None

        return Customer(name, contact, address, email)


class LoginWindow(QWidget):
    def __init__(self, parent_stack=None):
        super().__init__()
        self.stack = parent_stack
        self.setWindowTitle("Luqman Steel Trader - Login")
        self.setFixedSize(1980, 1080)  # Slightly more compact size

        # Set background gradient
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#1a2980"))  # Dark blue
        gradient.setColorAt(1, QColor("#26d0ce"))  # Teal
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(120, 70, 120, 70)

        # Logo Container
        logo_container = QFrame()
        logo_container.setFixedSize(150, 150)
        logo_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 75px;
                padding: 15px;
            }
        """)

        self.logo = QLabel(logo_container)
        pixmap = QPixmap("logo.png")
        if pixmap.isNull():
            self.logo.setText("LST")
            self.logo.setStyleSheet("font-size: 40px; color: #1a2980; font-weight: bold;")
        else:
            pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setGeometry(15, 15, 120, 120)

        main_layout.addWidget(logo_container, alignment=Qt.AlignCenter)

        # Welcome Label
        welcome_label = QLabel("LUQMAN STEEL & TRADERS")
        welcome_label.setFont(QFont("Arial", 24, QFont.Bold))
        welcome_label.setStyleSheet("color: white; letter-spacing: 2px;")
        welcome_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(welcome_label)

        # Subtitle
        subtitle = QLabel("Management System")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setStyleSheet("color: rgba(255,255,255,0.8);")
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)

        # Spacer
        main_layout.addSpacing(30)

        # Login Card
        login_card = QFrame()
        login_card.setFixedWidth(700)
        login_card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 12px;
                padding: 30px;
                border: none;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            }
            QLabel {
                color: #333;
                font-size: 14px;
            }
        """)

        login_layout = QVBoxLayout(login_card)
        login_layout.setSpacing(20)

        # Title
        login_title = QLabel("ADMIN LOGIN")
        login_title.setFont(QFont("Arial", 16, QFont.Bold))
        login_title.setStyleSheet("color: #1a2980;")
        login_title.setAlignment(Qt.AlignCenter)
        login_layout.addWidget(login_title)

        # Form
        form = QFormLayout()
        form.setVerticalSpacing(15)
        form.setHorizontalSpacing(20)

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Enter your username")
        self.username_edit.setStyleSheet("""
            QLineEdit {
                padding: 12px 15px;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #1a2980;
            }
        """)

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("Enter your password")
        self.password_edit.setStyleSheet(self.username_edit.styleSheet())

        form.addRow("Username:", self.username_edit)
        form.addRow("Password:", self.password_edit)
        login_layout.addLayout(form)

        # Message Label
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        login_layout.addWidget(self.message_label)

        # Login Button
        self.login_btn = QPushButton("LOGIN")
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a2980;
                color: white;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #0f1a5a;
            }
            QPushButton:pressed {
                background-color: #26d0ce;
            }
        """)
        self.login_btn.clicked.connect(self.handle_login)
        login_layout.addWidget(self.login_btn)

        # Connect Enter key to login
        self.username_edit.returnPressed.connect(self.handle_login)
        self.password_edit.returnPressed.connect(self.handle_login)

        main_layout.addWidget(login_card)
        self.setLayout(main_layout)

    def handle_login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        if username == "admin" and password == "password":
            self.message_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
            self.message_label.setText("Login successful!")
            if self.stack:
                self.stack.setCurrentIndex(1)
        else:
            self.message_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
            self.message_label.setText("Invalid username or password.")

            # Shake animation for wrong credentials
            self.shake_login()

    def shake_login(self):
        anim = QPropertyAnimation(self.login_btn, b"pos")
        anim.setDuration(300)
        anim.setKeyValueAt(0, self.login_btn.pos())
        anim.setKeyValueAt(0.2, self.login_btn.pos() + QPoint(10, 0))
        anim.setKeyValueAt(0.4, self.login_btn.pos() + QPoint(-10, 0))
        anim.setKeyValueAt(0.6, self.login_btn.pos() + QPoint(10, 0))
        anim.setKeyValueAt(0.8, self.login_btn.pos() + QPoint(-10, 0))
        anim.setKeyValueAt(1, self.login_btn.pos())
        anim.start()


class DashboardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_main = parent
        self.dark_mode = False
        self.init_ui()

    def init_ui(self):
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(25)

        # Header
        header = QHBoxLayout()

        # Title
        title = QLabel("Dashboard Overview")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        header.addWidget(title)

        # Spacer
        header.addStretch()

        # Theme toggle
        self.theme_toggle_btn = QPushButton()
        self.theme_toggle_btn.setFixedSize(40, 40)
        self.theme_toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a2980;
                border-radius: 20px;
                border: none;
                color: white;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #0f1a5a;
            }
        """)
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        header.addWidget(self.theme_toggle_btn)

        layout.addLayout(header)

        # Cards Grid
        cards_grid = QGridLayout()
        cards_grid.setHorizontalSpacing(20)
        cards_grid.setVerticalSpacing(20)

        # Card 1 - Income
        self.total_income_card = self._create_summary_card(
            "Total Income", "💰", "#2ecc71", "0.00 PKR", "Total income received"
        )
        cards_grid.addWidget(self.total_income_card, 0, 0)

        # Card 2 - Expense
        self.total_expense_card = self._create_summary_card(
            "Total Expense", "💸", "#e74c3c", "0.00 PKR", "Total expenses paid"
        )
        cards_grid.addWidget(self.total_expense_card, 0, 1)

        # Card 3 - Inventory
        self.inventory_value_card = self._create_summary_card(
            "Inventory Value", "📦", "#3498db", "0.00 PKR", "Current stock value"
        )
        cards_grid.addWidget(self.inventory_value_card, 1, 0)

        # Card 4 - Customers
        self.total_customers_card = self._create_summary_card(
            "Total Customers", "👥", "#f39c12", "0", "Registered customers"
        )
        cards_grid.addWidget(self.total_customers_card, 1, 1)

        layout.addLayout(cards_grid)

        # Recent Activity Section
        recent_activity_label = QLabel("Recent Activity")
        recent_activity_label.setFont(QFont("Arial", 16, QFont.Bold))
        recent_activity_label.setStyleSheet("color: #2c3e50; margin-top: 20px;")
        layout.addWidget(recent_activity_label)

        # Recent Activity Table
        self.recent_activity_table = QTableWidget(5, 3)
        self.recent_activity_table.setHorizontalHeaderLabels(["Date", "Activity", "Amount"])
        self.recent_activity_table.horizontalHeader().setStretchLastSection(True)
        self.recent_activity_table.verticalHeader().setVisible(False)
        self.recent_activity_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.recent_activity_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.recent_activity_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 5px;
                background-color: white;
                alternate-background-color: #f9f9f9;
            }
            QHeaderView::section {
                background-color: #1a2980;
                color: white;
                padding: 8px;
                border: none;
            }
        """)
        layout.addWidget(self.recent_activity_table)

        layout.addStretch()
        self.setLayout(layout)

    def _create_summary_card(self, title, icon, color, value, tooltip):
        card = QFrame()
        card.setFixedHeight(150)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                border-left: 5px solid {color};
                padding: 15px;
            }}
            QFrame:hover {{
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }}
        """)
        card.setToolTip(tooltip)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Top row (icon and title)
        top_row = QHBoxLayout()

        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 24px; color: {color};")
        top_row.addWidget(icon_label)

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #555;")
        top_row.addWidget(title_label)
        top_row.addStretch()

        layout.addLayout(top_row)

        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #333;")
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)

        # Bottom border effect
        bottom_border = QFrame()
        bottom_border.setFrameShape(QFrame.HLine)
        bottom_border.setStyleSheet(f"color: {color};")
        bottom_border.setFixedHeight(2)
        layout.addWidget(bottom_border)

        # Add animation
        self._add_card_animation(card)

        return card

    def _add_card_animation(self, card):
        # Fade-in animation
        opacity_effect = QGraphicsOpacityEffect(card)
        card.setGraphicsEffect(opacity_effect)
        fade_anim = QPropertyAnimation(opacity_effect, b"opacity")
        fade_anim.setDuration(800)
        fade_anim.setStartValue(0)
        fade_anim.setEndValue(1)
        fade_anim.setEasingCurve(QEasingCurve.InOutQuad)
        fade_anim.start()

    def update_dashboard_data(self):
        if self.parent_main:
            financial_records = self.parent_main.financial.records
            inventory_items = self.parent_main.inventory.items
            customers = self.parent_main.customer.customers

            total_income = sum(r.amount for r in financial_records if r.record_type == "Income")
            total_expense = sum(r.amount for r in financial_records if r.record_type == "Expense")
            total_inventory_value = sum(item.quantity * item.unit_price for item in inventory_items)
            num_customers = len(customers)

            # Update card values
            self._update_card_value(self.total_income_card, f"{total_income:,.2f} PKR")
            self._update_card_value(self.total_expense_card, f"{total_expense:,.2f} PKR")
            self._update_card_value(self.inventory_value_card, f"{total_inventory_value:,.2f} PKR")
            self._update_card_value(self.total_customers_card, f"{num_customers:,}")

            # Update recent activity
            self._update_recent_activity(financial_records)

    def _update_card_value(self, card, value):
        # Find the value label in the card's layout
        for i in range(card.layout().count()):
            widget = card.layout().itemAt(i).widget()
            if isinstance(widget, QLabel) and widget.styleSheet().find("28px") != -1:
                widget.setText(value)
                break

    def _update_recent_activity(self, records):
        self.recent_activity_table.setRowCount(0)
        recent_records = sorted(records, key=lambda r: r.date.toPyDate(), reverse=True)[:5]

        for record in recent_records:
            row = self.recent_activity_table.rowCount()
            self.recent_activity_table.insertRow(row)

            # Date
            date_item = QTableWidgetItem(record.date.toString("yyyy-MM-dd"))
            date_item.setTextAlignment(Qt.AlignCenter)
            self.recent_activity_table.setItem(row, 0, date_item)

            # Description
            desc_item = QTableWidgetItem(record.description)
            self.recent_activity_table.setItem(row, 1, desc_item)

            # Amount with color coding
            amount_item = QTableWidgetItem(f"{record.amount:,.2f} PKR")
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if record.record_type == "Income":
                amount_item.setForeground(QColor("#2ecc71"))  # Green for income
            else:
                amount_item.setForeground(QColor("#e74c3c"))  # Red for expense
            self.recent_activity_table.setItem(row, 2, amount_item)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.setStyleSheet("""
                QWidget {
                    background-color: #2c3e50;
                    color: #ecf0f1;
                }
                QFrame {
                    background-color: #34495e;
                }
                QTableWidget {
                    background-color: #34495e;
                    color: #ecf0f1;
                }
                QHeaderView::section {
                    background-color: #1a2980;
                    color: white;
                }
            """)
            self.theme_toggle_btn.setText("🌞")
        else:
            self.setStyleSheet("")
            self.theme_toggle_btn.setText("🌙")


# ... [Keep all your other existing classes: FinancialWidget, InventoryWidget, CustomerWidget, ReportsWidget, MainWindow] ...
class FinancialWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.records = []

        layout = QVBoxLayout()
        title = QLabel("Financial Management")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #1E90FF;")
        layout.addWidget(title)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Date", "Description", "Amount (PKR)", "Type"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setSelectionMode(self.table.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Transaction")
        self.add_btn.clicked.connect(self.add_record)
        btn_layout.addWidget(self.add_btn)

        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self.delete_record)
        btn_layout.addWidget(self.delete_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def add_record(self):
        dialog = FinancialDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            record = dialog.get_data()
            if record:
                self.records.append(record)
                self.refresh_table()
                # Update dashboard after data change
                if isinstance(self.parent(), MainWindow):
                    self.parent().dashboard.update_dashboard_data()


    def delete_record(self):
        selected = self.table.currentRow()
        if selected >= 0:
            descr = self.table.item(selected,1).text()
            reply = QMessageBox.question(self, "Confirm Delete", f"Delete the transaction '{descr}'?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.records.pop(selected)
                self.refresh_table()
                # Update dashboard after data change
                if isinstance(self.parent(), MainWindow):
                    self.parent().dashboard.update_dashboard_data()
        else:
            QMessageBox.information(self, "Information", "Select a transaction to delete.")

    def refresh_table(self):
        self.table.setRowCount(0)
        for record in sorted(self.records, key=lambda r: r.date.toPyDate(), reverse=True):
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(record.date.toString("yyyy-MM-dd")))
            self.table.setItem(row, 1, QTableWidgetItem(record.description))
            self.table.setItem(row, 2, QTableWidgetItem(f"{record.amount:,.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(record.record_type))


class InventoryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = []

        layout = QVBoxLayout()
        title = QLabel("Inventory Management")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #1E90FF;")
        layout.addWidget(title)

        self.table = QTableWidget(0,5)
        self.table.setHorizontalHeaderLabels(["Product Name", "Quantity", "Unit Price (PKR)", "Supplier", "Last Updated"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setSelectionMode(self.table.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Item")
        self.add_btn.clicked.connect(self.add_item)
        btn_layout.addWidget(self.add_btn)

        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self.delete_item)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def add_item(self):
        dialog = InventoryDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            item = dialog.get_data()
            if item:
                self.items.append(item)
                self.refresh_table()
                # Update dashboard after data change
                if isinstance(self.parent(), MainWindow):
                    self.parent().dashboard.update_dashboard_data()

    def delete_item(self):
        selected = self.table.currentRow()
        if selected >= 0:
            name = self.table.item(selected,0).text()
            reply = QMessageBox.question(self, "Confirm Delete", f"Delete the item '{name}'?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.items.pop(selected)
                self.refresh_table()
                # Update dashboard after data change
                if isinstance(self.parent(), MainWindow):
                    self.parent().dashboard.update_dashboard_data()
        else:
            QMessageBox.information(self, "Information", "Select an item to delete.")

    def refresh_table(self):
        self.table.setRowCount(0)
        for item in sorted(self.items, key=lambda i: i.name):
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row,0,QTableWidgetItem(item.name))
            self.table.setItem(row,1,QTableWidgetItem(str(item.quantity)))
            self.table.setItem(row,2,QTableWidgetItem(f"{item.unit_price:,.2f}"))
            self.table.setItem(row,3,QTableWidgetItem(item.supplier))
            self.table.setItem(row,4,QTableWidgetItem(item.last_updated.toString("yyyy-MM-dd")))


class CustomerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.customers = []

        layout = QVBoxLayout()
        title = QLabel("Customer Record Management")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #1E90FF;")
        layout.addWidget(title)

        self.table = QTableWidget(0,4)
        self.table.setHorizontalHeaderLabels(["Customer Name", "Contact Number", "Address", "Email"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setSelectionMode(self.table.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Customer")
        self.add_btn.clicked.connect(self.add_customer)
        btn_layout.addWidget(self.add_btn)

        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self.delete_customer)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def add_customer(self):
        dialog = CustomerDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            customer = dialog.get_data()
            if customer:
                self.customers.append(customer)
                self.refresh_table()
                # Update dashboard after data change
                if isinstance(self.parent(), MainWindow):
                    self.parent().dashboard.update_dashboard_data()

    def delete_customer(self):
        selected = self.table.currentRow()
        if selected >= 0:
            name = self.table.item(selected,0).text()
            reply = QMessageBox.question(self, "Confirm Delete", f"Delete the customer '{name}'?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.customers.pop(selected)
                self.refresh_table()
                # Update dashboard after data change
                if isinstance(self.parent(), MainWindow):
                    self.parent().dashboard.update_dashboard_data()
        else:
            QMessageBox.information(self, "Information", "Select a customer to delete.")

    def refresh_table(self):
        self.table.setRowCount(0)
        for cust in sorted(self.customers, key=lambda c: c.name):
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row,0,QTableWidgetItem(cust.name))
            self.table.setItem(row,1,QTableWidgetItem(cust.contact_number))
            self.table.setItem(row,2,QTableWidgetItem(cust.address))
            self.table.setItem(row,3,QTableWidgetItem(cust.email))


class ReportsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_main = parent # Reference to the MainWindow to access data
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Reports Generation")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color: #00468C;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Report Options
        options_layout = QFormLayout()

        self.report_type_combo = QComboBox()
        self.report_type_combo.addItems(["Financial Summary", "Inventory Summary", "Customer List"])
        options_layout.addRow("Select Report Type:", self.report_type_combo)

        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate().addMonths(-1)) # Default to last month
        options_layout.addRow("Start Date (Financial Only):", self.start_date_edit)

        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())
        options_layout.addRow("End Date (Financial Only):", self.end_date_edit)

        layout.addLayout(options_layout)

        self.generate_report_btn = QPushButton("Generate Report")
        self.generate_report_btn.setFixedHeight(40)
        self.generate_report_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E90FF;
                color: white;
                border-radius: 5px;
                font-size: 14pt;
            }
            QPushButton:hover {
                background-color: #0c69e5;
            }
        """)
        self.generate_report_btn.clicked.connect(self.generate_report)
        layout.addWidget(self.generate_report_btn)

        # Report Display Area
        self.report_text_area = QTextEdit()
        self.report_text_area.setReadOnly(True)
        self.report_text_area.setFont(QFont("Courier New", 10))
        self.report_text_area.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        layout.addWidget(self.report_text_area)

        layout.addStretch()
        self.setLayout(layout)

    def generate_report(self):
        report_type = self.report_type_combo.currentText()
        report_output = ""

        if report_type == "Financial Summary":
            start_date = self.start_date_edit.date()
            end_date = self.end_date_edit.date()
            financial_records = self.parent_main.financial.records

            filtered_records = [r for r in financial_records if start_date <= r.date <= end_date]
            total_income = sum(r.amount for r in filtered_records if r.record_type == "Income")
            total_expense = sum(r.amount for r in filtered_records if r.record_type == "Expense")
            net_profit_loss = total_income - total_expense

            report_output += f"--- Financial Summary Report ({start_date.toString('yyyy-MM-dd')} to {end_date.toString('yyyy-MM-dd')}) ---\n"
            report_output += f"{'Total Income:':<20} {total_income:,.2f} PKR\n"
            report_output += f"{'Total Expense:':<20} {total_expense:,.2f} PKR\n"
            report_output += f"{'Net Profit/Loss:':<20} {net_profit_loss:,.2f} PKR\n"
            report_output += "\n--- Detailed Transactions ---\n"
            report_output += f"{'Date':<12} {'Type':<8} {'Amount':>15} {'Description':<30}\n"
            report_output += "-" * 70 + "\n"
            for record in sorted(filtered_records, key=lambda r: r.date.toPyDate()):
                report_output += f"{record.date.toString('yyyy-MM-dd'):<12} {record.record_type:<8} {record.amount:>15,.2f} {record.description:<30}\n"

        elif report_type == "Inventory Summary":
            inventory_items = self.parent_main.inventory.items
            total_inventory_value = sum(item.quantity * item.unit_price for item in inventory_items)
            total_items = sum(item.quantity for item in inventory_items)

            report_output += "--- Inventory Summary Report ---\n"
            report_output += f"{'Total Unique Items:':<20} {len(inventory_items)}\n"
            report_output += f"{'Total Quantity on Hand:':<20} {total_items}\n"
            report_output += f"{'Total Inventory Value:':<20} {total_inventory_value:,.2f} PKR\n"
            report_output += "\n--- Detailed Inventory ---\n"
            report_output += f"{'Product Name':<25} {'Qty':>8} {'Unit Price':>15} {'Supplier':<20}\n"
            report_output += "-" * 70 + "\n"
            for item in sorted(inventory_items, key=lambda i: i.name):
                report_output += f"{item.name:<25} {item.quantity:>8} {item.unit_price:>15,.2f} {item.supplier:<20}\n"

        elif report_type == "Customer List":
            customers = self.parent_main.customer.customers
            report_output += "--- Customer List Report ---\n"
            report_output += f"{'Total Customers:':<20} {len(customers)}\n"
            report_output += "\n--- Detailed Customer Information ---\n"
            report_output += f"{'Name':<25} {'Contact':<15} {'Email':<30}\n"
            report_output += "-" * 70 + "\n"
            for cust in sorted(customers, key=lambda c: c.name):
                report_output += f"{cust.name:<25} {cust.contact_number:<15} {cust.email if cust.email else 'N/A':<30}\n"

        self.report_text_area.setPlainText(report_output)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Luqman Steel Trader Management System")
        self.setGeometry(100, 100, 1100, 700)

        # Central widget - stacked widget to switch pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Pages
        # In MainWindow
        self.login_page = LoginWindow(parent_stack=self.stacked_widget)

        # Pass self (MainWindow) to widgets that need to access other widgets' data
        self.dashboard = DashboardWidget(self)
        self.financial = FinancialWidget(self)
        self.inventory = InventoryWidget(self)
        self.customer = CustomerWidget(self)
        self.reports = ReportsWidget(self) # Pass self to ReportsWidget too

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.create_main_widget())

        self.stacked_widget.setCurrentIndex(0)  # start with login

    def create_main_widget(self):
        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)

        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout()
        sidebar.setStyleSheet("background-color: #1E90FF;")
        sidebar.setLayout(sidebar_layout)

        btn_dashboard = QPushButton("Dashboard")
        btn_financial = QPushButton("Financial")
        btn_inventory = QPushButton("Inventory")
        btn_customer = QPushButton("Customers")
        btn_reports = QPushButton("Reports")
        btn_logout = QPushButton("Logout")

        # Styling buttons
        for btn in [btn_dashboard, btn_financial, btn_inventory, btn_customer, btn_reports, btn_logout]:
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    color: white;
                    background-color: #1E90FF;
                    border: none;
                    text-align: left;
                    padding-left: 20px;
                    font-size: 14pt;
                }
                QPushButton:hover {
                    background-color: #0c69e5;
                }
            """)

        sidebar_layout.addWidget(btn_dashboard)
        sidebar_layout.addWidget(btn_financial)
        sidebar_layout.addWidget(btn_inventory)
        sidebar_layout.addWidget(btn_customer)
        sidebar_layout.addWidget(btn_reports)
        sidebar_layout.addStretch()
        sidebar_layout.addWidget(btn_logout)

        # Content area stacked widget
        self.content_stack = QStackedWidget()
        self.content_stack.addWidget(self.dashboard)
        self.content_stack.addWidget(self.financial)
        self.content_stack.addWidget(self.inventory)
        self.content_stack.addWidget(self.customer)
        self.content_stack.addWidget(self.reports)

        layout.addWidget(sidebar)
        layout.addWidget(self.content_stack)

        # Connect sidebar buttons to pages
        btn_dashboard.clicked.connect(lambda: self.switch_page(0))
        btn_financial.clicked.connect(lambda: self.switch_page(1))
        btn_inventory.clicked.connect(lambda: self.switch_page(2))
        btn_customer.clicked.connect(lambda: self.switch_page(3))
        btn_reports.clicked.connect(lambda: self.switch_page(4))
        btn_logout.clicked.connect(self.logout)

        return widget

    def switch_page(self, index):
        self.content_stack.setCurrentIndex(index)
        # When switching to dashboard, update its data
        if index == 0: # Dashboard index
            self.dashboard.update_dashboard_data()


    def logout(self):
        reply = QMessageBox.question(self, "Logout Confirmation", "Are you sure you want to logout?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.stacked_widget.setCurrentIndex(0)  # back to login

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Set default font
    font = QFont("Arial", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()