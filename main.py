import sys
import mysql.connector
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
    QPushButton, QStackedWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QLineEdit, QComboBox, QDialog, QFormLayout, QTextEdit,
    QMessageBox, QDateEdit, QListWidget, QListWidgetItem, QScrollArea, QFrame,
    QTabWidget
)
from PySide6.QtCore import Qt, QDate, QDateTime
from PySide6.QtGui import QFont, QColor

# --- Database Configuration ---
# IMPORTANT: Replace these with your actual MySQL database credentials
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'A2d3e5l7',
    'database': 'crm'
}

# --- Qt Style Sheet (QSS) for Modern, Minimalistic UI ---
QSS = """
QMainWindow {
    background-color: #f0f2f5; /* Light gray background */
}

/* Sidebar Styling */
#sidebar {
    background-color: #2c3e50; /* Dark blue-gray */
    border-right: 1px solid #34495e;
    padding: 15px;
    border-radius: 8px;
}

#sidebar QLabel {
    color: #ecf0f1; /* Light text */
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 20px;
}

#sidebar QPushButton {
    background-color: #34495e; /* Slightly lighter dark blue-gray */
    color: #ecf0f1;
    border: none;
    padding: 12px 15px;
    text-align: left;
    font-size: 16px;
    border-radius: 6px;
    margin-bottom: 8px;
    transition: background-color 0.3s ease;
}

#sidebar QPushButton:hover {
    background-color: #4a627a; /* Lighter on hover */
}

#sidebar QPushButton:checked {
    background-color: #3498db; /* Primary blue for active */
    font-weight: bold;
}

/* Content Area Styling */
#contentArea {
    background-color: #ffffff; /* White background for content */
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

QLabel {
    font-family: "Inter", sans-serif;
    color: #333;
}

/* Page Titles */
.page-title {
    font-size: 28px;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 20px;
    border-bottom: 2px solid #e0e0e0;
    padding-bottom: 10px;
}

/* General Buttons */
QPushButton {
    background-color: #3498db; /* Primary blue */
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 6px;
    font-size: 15px;
    font-weight: 500;
    transition: background-color 0.3s ease;
}

QPushButton:hover {
    background-color: #2980b9; /* Darker blue on hover */
}

QPushButton:pressed {
    background-color: #21618c;
}

/* Danger Buttons (e.g., Delete) */
QPushButton.danger {
    background-color: #e74c3c; /* Red */
}
QPushButton.danger:hover {
    background-color: #c0392b;
}

/* Input Fields */
QLineEdit, QTextEdit, QComboBox, QDateEdit {
    border: 1px solid #bdc3c7; /* Light gray border */
    border-radius: 5px;
    padding: 8px 10px;
    font-size: 14px;
    background-color: #fdfefe;
    color: #2c3e50; /* Dark text color */
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {
    border-color: #3498db; /* Primary blue on focus */
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

QComboBox::drop-down {
    border: 0px; /* No border for the dropdown arrow */
}
QComboBox::down-arrow {
    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTcgMTBMMTIgMTVMMTcgMTBaIiBmaWxsPSIjNjk2OTY5Ii8+Cjwvc3ZnPg==); /* Simple SVG down arrow */
    width: 16px;
    height: 16px;
    margin-right: 5px;
}

/* Table Widget */
QTableWidget {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 14px;
    selection-background-color: #d4edda; /* Light green for selection */
    selection-color: #2c3e50;
}

QHeaderView::section {
    background-color: #ecf0f1; /* Light header background */
    padding: 10px;
    border-bottom: 1px solid #bdc3c7;
    font-weight: bold;
    font-size: 14px;
    color: #2c3e50;
}

QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #f0f0f0;
}

QTableWidget::item:selected {
    background-color: #e8f5e9; /* Lighter green for selected item */
}

/* Scroll Area */
QScrollArea {
    border: none;
}
QScrollArea > QWidget > QWidget {
    background-color: transparent; /* Ensure content background is transparent */
}

/* Form Layout Labels - REVISED FOR CLARITY */
QFormLayout QLabel {
    font-weight: bold; /* Make labels more prominent */
    color: #2c3e50; /* Darker color for better contrast */
    margin-bottom: 5px;
}

/* Message Boxes */
QMessageBox {
    background-color: #ffffff;
    border-radius: 8px;
    padding: 20px;
    font-size: 15px;
}
QMessageBox QPushButton {
    min-width: 80px;
    padding: 8px 12px;
}
QMessageBox QLabel {
    color: #333;
}

/* Specific elements for Dashboard */
#kpiLabel {
    font-size: 18px;
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 5px;
}
#kpiValue {
    font-size: 32px;
    font-weight: bold;
    color: #3498db; /* Primary blue */
}
.kpi-card {
    background-color: #fdfdfd;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 15px;
    margin: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

/* Customer Profile Styling */
#profileHeader {
    background-color: #ecf0f1;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    border: 1px solid #bdc3c7;
}
#profileHeader QLabel {
    font-size: 18px;
    font-weight: bold;
    color: #2c3e50;
}
#profileHeader QLabel[property="value"] {
    font-weight: normal;
    font-size: 16px;
    color: #555;
}
.profile-section-title {
    font-size: 20px;
    font-weight: bold;
    color: #2c3e50;
    margin-top: 20px;
    margin-bottom: 10px;
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 5px;
}
.profile-info-label {
    font-weight: 500;
    color: #555;
}
.profile-info-value {
    font-weight: normal;
    color: #333;
}

/* Login Dialog Specific Styling */
QDialog {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}
QDialog QLabel#title_label { /* Targeting the login dialog title */
    color: #2c3e50;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 25px;
}
QDialog QLabel#error_label { /* Targeting the error message */
    color: #e74c3c;
    font-size: 14px;
    margin-top: 10px;
}
QDialog QLineEdit {
    padding: 10px;
    font-size: 16px;
    border: 1px solid #bdc3c7;
    border-radius: 5px;
}
QDialog QPushButton {
    background-color: #3498db;
    color: white;
    padding: 12px 25px;
    border-radius: 8px;
    font-size: 18px;
    font-weight: bold;
    margin-top: 20px;
}
QDialog QPushButton:hover {
    background-color: #2980b9;
}
"""

# --- Database Manager Class ---
class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.connection = None

    def connect(self):
        """Establishes a database connection."""
        try:
            self.connection = mysql.connector.connect(**self.config)
            print("Database connection established.")
            return True
        except mysql.connector.Error as err:
            QMessageBox.critical(None, "Database Connection Error",
                                 f"Failed to connect to database:\n{err}")
            print(f"Database connection error: {err}")
            self.connection = None
            return False

    def close(self):
        """Closes the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None
            print("Database connection closed.")

    def execute_procedure(self, proc_name, params=None, fetch_one=False, fetch_all=False):
        """
        Executes a stored procedure and returns results.
        Automatically handles connection, cursor, and closing.
        """
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return None

        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True) # Return results as dictionaries
            print(f"Executing procedure: {proc_name}")
            print(f"Parameters: {params}")
            
            if params:
                cursor.callproc(proc_name, params)
            else:
                cursor.callproc(proc_name)

            # Fetch results if any
            result = None
            for res in cursor.stored_results():
                if fetch_one:
                    result = res.fetchone()
                    print(f"Fetch one result: {result}")
                elif fetch_all:
                    result = res.fetchall()
                    print(f"Fetch all results: {result}")
                else:
                    # If not explicitly fetching, just consume the result set
                    res.fetchall() # Consume all rows

            self.connection.commit() # Commit changes for DML procedures
            return result

        except mysql.connector.Error as err:
            error_msg = f"Error executing procedure '{proc_name}': {err}"
            print(error_msg)
            print(f"Error Code: {err.errno}")
            print(f"SQL State: {err.sqlstate}")
            print(f"Error Message: {err.msg}")
            QMessageBox.critical(None, "Database Error", error_msg)
            self.connection.rollback() # Rollback on error
            raise Exception(f"Database error: {err.msg}") # Re-raise with more context
        finally:
            if cursor:
                cursor.close()

    # --- Wrapper methods for specific stored procedures ---

    # Admin/Login Procedure
    def authenticateAdmin(self, username, password):
        return self.execute_procedure('authenticateAdmin', (username, password), fetch_one=True)

    # Dashboard Procedures
    def getTotalLeads(self):
        """Get total number of leads"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT getTotalLeads()")
            result = cursor.fetchone()
            cursor.close()
            return {'TotalLeads': result[0] if result else 0}
        except Exception as e:
            print(f"Error in getTotalLeads: {str(e)}")
            return None

    def getTotalCustomers(self):
        """Get total number of customers"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT getTotalCustomers()")
            result = cursor.fetchone()
            print(f"Raw result from getTotalCustomers: {result}")  # Debug print
            cursor.close()
            return {'TotalCustomers': result[0] if result else 0}
        except Exception as e:
            print(f"Error in getTotalCustomers: {str(e)}")
            return None

    def getTotalConversions(self):
        return self.execute_procedure('getTotalConversions', fetch_one=True)

    def getActiveCampaignsCount(self):
        return self.execute_procedure('getActiveCampaignsCount', fetch_one=True)

    def getFollowUpsDueToday(self, emp_id=None):
        return self.execute_procedure('getFollowUpsDueToday', (emp_id,), fetch_all=True)

    def getStatusCounts(self):
        return self.execute_procedure('getStatusCounts', fetch_all=True)

    def getAllCampaigns(self):
        """Get all campaigns with their sources"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.*, COUNT(s.sourceID) as sourceCount 
                FROM campaign c 
                LEFT JOIN source s ON c.campaignID = s.campaignID 
                GROUP BY c.campaignID
            """)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error in getAllCampaigns: {str(e)}")
            return None

    def getRecentFollowUps(self, limit=5):
        return self.execute_procedure('getRecentFollowUps', (limit,), fetch_all=True)

    # Leads Module Procedures
    def getLeads(self, emp_id=None, status_id=None, start_date=None, end_date=None):
        """Get leads with all necessary fields for editing and converting"""
        try:
            result = self.execute_procedure('getLeads1', (emp_id, status_id, start_date, end_date), fetch_all=True)
            if result:
                print(f"Retrieved {len(result)} leads with fields: {result[0].keys() if result else 'No leads'}")
            return result
        except Exception as e:
            print(f"Error in getLeads: {str(e)}")
            return None

    def createLead(self, person_id, source_id, emp_id, status_id, notes):
        """
        Creates a new lead in the database.
        Returns True if successful, False otherwise.
        """
        try:
            result = self.execute_procedure('createLead', (person_id, source_id, emp_id, status_id, notes))
            print(f"Create lead result: {result}")
            return True
        except Exception as e:
            print(f"Error in createLead: {str(e)}")
            return False

    def updateLead(self, lead_id, new_source_id, new_status_id, new_emp_id, new_notes):
        """
        Updates an existing lead in the database.
        Returns True if successful, False otherwise.
        """
        try:
            result = self.execute_procedure('updateLead', (lead_id, new_source_id, new_status_id, new_emp_id, new_notes))
            print(f"Update lead result: {result}")
            return True
        except Exception as e:
            print(f"Error in updateLead: {str(e)}")
            return False

    def deleteLead(self, lead_id):
        """
        Deletes a lead from the database.
        Returns True if successful, False otherwise.
        """
        try:
            result = self.execute_procedure('deleteLead', (lead_id,))
            print(f"Delete lead result: {result}")
            return True
        except Exception as e:
            print(f"Error in deleteLead: {str(e)}")
            return False

    def createPerson(self, name, email, phone):
        return self.execute_procedure('createPerson', (name, email, phone), fetch_one=True) # Returns newPersonID

    def updatePerson(self, person_id, name, email, phone):
        return self.execute_procedure('updatePerson', (person_id, name, email, phone))

    def getAllSources(self):
        """Get all sources with their campaign names"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT s.*, c.name as campaignName 
                FROM source s 
                LEFT JOIN campaign c ON s.campaignID = c.campaignID
            """)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error in getAllSources: {str(e)}")
            return None

    def getAllEmployees(self):
        """Get all employees with their person details"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT e.*, p.name as employeeName, p.email, p.phone 
                FROM employee e 
                JOIN person p ON e.personID = p.personID
            """)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error in getAllEmployees: {str(e)}")
            return None

    def getAllStatus(self):
        return self.execute_procedure('getAllStatus', fetch_all=True)

    def changeLeadStatus(self, lead_id, status_id):
        return self.execute_procedure('changeLeadStatus', (lead_id, status_id))

    def logStatusChange(self, lead_id, new_status_id, emp_id, notes):
        return self.execute_procedure('logStatusChange', (lead_id, new_status_id, emp_id, notes))

    def completeFollowUp(self, follow_up_id):
        return self.execute_procedure('completeFollowUp', (follow_up_id,))

    def getPendingFollowUps(self, emp_id=None, lead_id=None, before_date=None):
        # Ensure before_date is formatted correctly if not None
        # QDate and QDateTime objects need to be converted to string for MySQL
        formatted_before_date = None
        if isinstance(before_date, QDate):
            formatted_before_date = before_date.toString(Qt.ISODate)
        elif isinstance(before_date, QDateTime):
            formatted_before_date = before_date.toString(Qt.ISODate)
        elif before_date is not None:
            formatted_before_date = str(before_date) # Assume it's already a string or compatible type

        return self.execute_procedure('getPendingFollowUps', (emp_id, lead_id, formatted_before_date), fetch_all=True)

    # Customer Module Procedures
    def getAllCustomers(self, start_date=None, end_date=None, min_budget=None, max_budget=None, product_id=None):
        return self.execute_procedure('getAllCustomers', (start_date, end_date, min_budget, max_budget, product_id), fetch_all=True)

    def getCustomerDetailedProfile(self, cust_id):
        return self.execute_procedure('getCustomerDetailedProfile', (cust_id,), fetch_one=True)

    def getCustomerInteractions(self, cust_id):
        return self.execute_procedure('getCustomerInteractions', (cust_id,), fetch_all=True)

    def getCustomerProductInterests(self, cust_id):
        return self.execute_procedure('getCustomerProductInterests', (cust_id,), fetch_all=True)

    def getCustomerStatusJourney(self, cust_id):
        return self.execute_procedure('getCustomerStatusJourney', (cust_id,), fetch_all=True)

    def updateCustomerPreferences(self, cust_pref_id, contact_method_id, p_language, p_contact_time, p_budget):
        return self.execute_procedure('updateCustomerPreferences', (cust_pref_id, contact_method_id, p_language, p_contact_time, p_budget))

    def addCustomerProductInterest(self, cust_id, product_id):
        return self.execute_procedure('addCustomerProductInterest', (cust_id, product_id))

    def removeCustomerProductInterest(self, cust_id, product_id):
        return self.execute_procedure('removeCustomerProductInterest', (cust_id, product_id))

    def getAllContactMethods(self):
        return self.execute_procedure('getAllContactMethods', fetch_all=True)

    def getProducts(self):
        return self.execute_procedure('getProducts', fetch_all=True) # For product interest dropdown

    def deleteCustomer(self, cust_id):
        return self.execute_procedure('deleteCustomer', (cust_id,))

    # Campaigns & Sources Procedures
    def getSourcesForCampaign(self, campaign_id):
        return self.execute_procedure('getSourcesForCampaign', (campaign_id,), fetch_all=True)

    def getLeadsForCampaign(self, campaign_id):
        return self.execute_procedure('getLeadsForCampaign', (campaign_id,), fetch_all=True)

    def createSource(self, campaign_id, source_name, source_desc):
        return self.execute_procedure('createSource', (campaign_id, source_name, source_desc))

    def updateSource(self, source_id, new_campaign_id, new_source_name, new_source_desc):
        return self.execute_procedure('updateSource', (source_id, new_campaign_id, new_source_name, new_source_desc))

    def deleteSource(self, source_id):
        return self.execute_procedure('deleteSource', (source_id,))

    def deleteCampaign(self, campaign_id):
        return self.execute_procedure('deleteCampaign', (campaign_id,))

    # Products Procedures
    def addProduct(self, product_name, product_desc):
        return self.execute_procedure('addProduct', (product_name, product_desc))

    def updateProduct(self, product_id, product_name, product_desc):
        return self.execute_procedure('updateProduct', (product_id, product_name, product_desc))

    def deleteProduct(self, product_id):
        return self.execute_procedure('deleteProduct', (product_id,))

    # Employees Procedures
    def getEmployeeDetails(self, emp_id):
        return self.execute_procedure('getEmployeeDetails', (emp_id,), fetch_one=True)

    def createEmployee(self, person_id, role):
        return self.execute_procedure('createEmployee', (person_id, role))

    def updateEmployee(self, emp_id, new_role):
        return self.execute_procedure('updateEmployee', (emp_id, new_role))

    def deleteEmployee(self, emp_id):
        return self.execute_procedure('deleteEmployee', (emp_id,))

    # Follow-ups Procedures
    def getAllFollowUps(self):
        """Get all follow-ups with lead and employee details"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT f.*, 
                       p.name as leadName,
                       ep.name as employeeName
                FROM followUp f
                JOIN leads l ON f.leadID = l.leadID
                JOIN person p ON l.personID = p.personID
                JOIN employee e ON f.empID = e.empID
                JOIN person ep ON e.personID = ep.personID
            """)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error in getAllFollowUps: {str(e)}")
            return None

    # Reports/Analytics Procedures
    def getCampaignConversionFunnel(self, campaign_id):
        return self.execute_procedure('getCampaignConversionFunnel', (campaign_id,), fetch_all=True)

    def getSourceEffectiveness(self):
        return self.execute_procedure('getSourceEffectiveness', fetch_all=True)

    def createCustomer(self, lead_id, person_id):
        """
        Creates a new customer from a lead.
        Returns True if successful, False if lead is already converted or if there's an error.
        """
        try:
            result = self.execute_procedure('createCustomer', (lead_id, person_id), fetch_one=True)
            print(f"Create customer result: {result}")
            return result and result.get('success', False)
        except Exception as e:
            print(f"Error in createCustomer: {str(e)}")
            return False

    # Reports/Analytics Procedures
    def getAnalyticsData(self):
        """Get basic analytics data"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM leads) as totalLeads,
                    (SELECT COUNT(*) FROM customer) as totalCustomers,
                    (SELECT COUNT(*) FROM campaign) as totalCampaigns,
                    (SELECT COUNT(*) FROM employee) as totalEmployees,
                    (SELECT COUNT(*) FROM followUp WHERE completed = FALSE) as pendingFollowUps
            """)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            print(f"Error in getAnalyticsData: {str(e)}")
            return None


# --- Login Dialog ---
class LoginDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.setWindowTitle("Admin Login")
        self.setFixedSize(380, 280) # Slightly larger for better spacing
        self.setStyleSheet(QSS) # Apply global QSS

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("Admin Login")
        self.title_label.setObjectName("title_label") # For specific QSS targeting
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password) # Hide password

        self.form_layout.addRow("Username:", self.username_input)
        self.form_layout.addRow("Password:", self.password_input)
        self.layout.addLayout(self.form_layout)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.attempt_login)
        self.login_button.setFixedSize(180, 45) # Make button a bit larger
        self.layout.addWidget(self.login_button, alignment=Qt.AlignCenter)

        self.error_label = QLabel("")
        self.error_label.setObjectName("error_label") # For specific QSS targeting
        self.error_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.error_label)

    def attempt_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.error_label.setText("Please enter both username and password.")
            return

        admin_data = self.db.authenticateAdmin(username, password)

        if admin_data:
            QMessageBox.information(self, "Login Success", f"Welcome, {admin_data['username']}!")
            self.accept() # Close dialog with QDialog.Accepted
        else:
            self.error_label.setText("Invalid username or password.")
            self.password_input.clear() # Clear password field for security


# --- Dashboard Page ---
class DashboardPage(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.setObjectName("contentArea") # For QSS styling

        self.layout = QVBoxLayout(self)
        self.title = QLabel("Dashboard")
        self.title.setObjectName("page-title")
        self.layout.addWidget(self.title)

        self.kpi_grid = QHBoxLayout()
        self.layout.addLayout(self.kpi_grid)

        self.visuals_layout = QVBoxLayout()
        self.layout.addLayout(self.visuals_layout)

        self.refresh_button = QPushButton("Refresh Data")
        self.refresh_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.refresh_button)

        self.load_data()

    def create_kpi_card(self, title, value, unit=""):
        card = QFrame()
        card.setObjectName("kpi-card")
        card_layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setObjectName("kpiLabel")
        card_layout.addWidget(title_label)

        value_label = QLabel(f"{value}{unit}")
        value_label.setObjectName("kpiValue")
        card_layout.addWidget(value_label)
        return card

    def load_data(self):
        # Clear existing KPIs
        while self.kpi_grid.count():
            item = self.kpi_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Clear existing visuals
        while self.visuals_layout.count():
            item = self.visuals_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Fetch KPIs
        total_leads = self.db.getTotalLeads()
        total_customers = self.db.getTotalCustomers()
        print(f"Dashboard - Total Customers result: {total_customers}")  # Debug print
        total_conversions = self.db.getTotalConversions()
        active_campaigns = self.db.getActiveCampaignsCount()
        followups_due_today = self.db.getFollowUpsDueToday()

        self.kpi_grid.addWidget(self.create_kpi_card("Total Leads", total_leads['TotalLeads'] if total_leads else 0))
        self.kpi_grid.addWidget(self.create_kpi_card("Customers", total_customers['TotalCustomers'] if total_customers else 0))
        self.kpi_grid.addWidget(self.create_kpi_card("Conversions", total_conversions['TotalConversions'] if total_conversions else 0))
        self.kpi_grid.addWidget(self.create_kpi_card("Active Campaigns", active_campaigns['ActiveCampaigns'] if active_campaigns else 0))
        self.kpi_grid.addWidget(self.create_kpi_card("Follow-ups Today", len(followups_due_today) if followups_due_today else 0))

        # Visuals: Status Funnel (Text-based for simplicity)
        status_counts = self.db.getStatusCounts()
        if status_counts:
            status_label = QLabel("<h3 style='color: #2c3e50;'>Lead Status Funnel:</h3>")
            self.visuals_layout.addWidget(status_label)
            for row in status_counts:
                self.visuals_layout.addWidget(QLabel(f"- {row['statusName']}: {row['leadCount']} leads"))
        else:
            self.visuals_layout.addWidget(QLabel("No status data available."))

        # Visuals: Campaign Performance
        campaigns = self.db.getAllCampaigns()
        if campaigns:
            campaign_label = QLabel("<h3 style='color: #2c3e50; margin-top: 20px;'>Campaign Performance:</h3>")
            self.visuals_layout.addWidget(campaign_label)
            for campaign in campaigns:
                self.visuals_layout.addWidget(QLabel(f"- {campaign['name']}: {campaign['sourceCount']} sources"))
        else:
            self.visuals_layout.addWidget(QLabel("No campaign data available."))

        # Visuals: Recent Follow-ups
        recent_followups = self.db.getRecentFollowUps(limit=5)
        if recent_followups:
            followup_label = QLabel("<h3 style='color: #2c3e50; margin-top: 20px;'>Recent Follow-ups:</h3>")
            self.visuals_layout.addWidget(followup_label)
            for fu in recent_followups:
                status_text = "Completed" if fu['completed'] else "Pending"
                self.visuals_layout.addWidget(QLabel(f"- {fu['followUpDate'].strftime('%Y-%m-%d')}: {fu['notes']} (Lead: {fu['leadPersonName']}, Emp: {fu['assignedEmployee']}) - {status_text}"))
        else:
            self.visuals_layout.addWidget(QLabel("No recent follow-up data."))

        self.layout.addStretch(1) # Push content to top


# --- Lead Form Dialog (for Create/Update) ---
class LeadFormDialog(QDialog):
    def __init__(self, db_manager, lead_data=None, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.lead_data = lead_data
        self.person_id = lead_data.get('personID') if lead_data else None
        self.setWindowTitle("Edit Lead" if lead_data else "Create New Lead")
        self.setMinimumWidth(400)
        self.setStyleSheet(QSS)

        print(f"Initializing LeadFormDialog with data: {lead_data}")  # Debug print

        self.layout = QFormLayout(self)

        # Person Details (Name, Email, Phone)
        self.person_name_input = QLineEdit(lead_data.get('leadName', '') if lead_data else "")
        self.person_email_input = QLineEdit(lead_data.get('email', '') if lead_data else "")
        self.person_phone_input = QLineEdit(lead_data.get('phone', '') if lead_data else "")
        self.layout.addRow("Person Name:", self.person_name_input)
        self.layout.addRow("Email:", self.person_email_input)
        self.layout.addRow("Phone:", self.person_phone_input)

        # Lead Details
        self.source_combo = QComboBox()
        self.status_combo = QComboBox()
        self.employee_combo = QComboBox()
        self.notes_input = QTextEdit(lead_data.get('notes', '') if lead_data else "")

        self.layout.addRow("Source:", self.source_combo)
        self.layout.addRow("Status:", self.status_combo)
        self.layout.addRow("Assigned Employee:", self.employee_combo)
        self.layout.addRow("Notes:", self.notes_input)

        self.load_dropdown_data()

        if lead_data:
            # Set initial selections for existing lead
            print(f"Setting initial selections for lead: {lead_data}")  # Debug print
            self._set_combo_selection(self.source_combo, lead_data.get('sourceID'))
            self._set_combo_selection(self.status_combo, lead_data.get('statusID'))
            self._set_combo_selection(self.employee_combo, lead_data.get('empID'))

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_lead)
        self.layout.addRow(self.save_button)

    def _set_combo_selection(self, combo_box, value_id):
        """Helper to set QComboBox selection by data ID."""
        if value_id is None:
            return
        for i in range(combo_box.count()):
            if combo_box.itemData(i) == value_id:
                combo_box.setCurrentIndex(i)
                return

    def load_dropdown_data(self):
        sources = self.db.getAllSources()
        if sources:
            self.source_combo.addItem("Select Source", None)
            for s in sources:
                self.source_combo.addItem(s['sourceName'], s['sourceID'])

        statuses = self.db.getAllStatus()
        if statuses:
            self.status_combo.addItem("Select Status", None)
            for s in statuses:
                self.status_combo.addItem(s['statusName'], s['statusID'])

        employees = self.db.getAllEmployees()
        if employees:
            self.employee_combo.addItem("Select Employee", None)
            for e in employees:
                self.employee_combo.addItem(e['employeeName'], e['empID'])

    def save_lead(self):
        person_name = self.person_name_input.text().strip()
        person_email = self.person_email_input.text().strip()
        person_phone = self.person_phone_input.text().strip()
        source_id = self.source_combo.currentData()
        status_id = self.status_combo.currentData()
        employee_id = self.employee_combo.currentData()
        notes = self.notes_input.toPlainText().strip()

        print(f"Saving lead with data:")
        print(f"Person Name: {person_name}")
        print(f"Person Email: {person_email}")
        print(f"Person Phone: {person_phone}")
        print(f"Source ID: {source_id}")
        print(f"Status ID: {status_id}")
        print(f"Employee ID: {employee_id}")
        print(f"Notes: {notes}")

        if not (person_name and source_id and status_id and employee_id):
            QMessageBox.warning(self, "Input Error", "Please fill in all required fields (Person Name, Source, Status, Employee).")
            return

        if self.lead_data: # Update existing lead
            print("Updating existing lead...")
            # Update person details
            if self.person_id:
                person_success = self.db.updatePerson(self.person_id, person_name, person_email, person_phone)
                print(f"Person update result: {person_success}")
            else:
                print("Warning: No personID found for update")
                QMessageBox.warning(self, "Warning", "Could not update person details: Person ID missing.")
                return

            # Update lead details
            lead_success = self.db.updateLead(
                self.lead_data['leadID'],
                source_id,
                status_id,
                employee_id,
                notes
            )
            print(f"Lead update result: {lead_success}")

            if lead_success is not None:
                QMessageBox.information(self, "Success", "Lead updated successfully!")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Failed to update lead. Please check the console for details.")

        else: # Create new lead
            print("Creating new lead...")
            # First, create the person
            new_person_result = self.db.createPerson(person_name, person_email, person_phone)
            print(f"Person creation result: {new_person_result}")
            
            if new_person_result and 'newPersonID' in new_person_result:
                new_person_id = new_person_result['newPersonID']
                print(f"New person ID: {new_person_id}")
                
                # Then, create the lead
                success = self.db.createLead(
                    new_person_id,
                    source_id,
                    employee_id,
                    status_id,
                    notes
                )
                print(f"Lead creation result: {success}")
                
                if success:
                    QMessageBox.information(self, "Success", "Lead created successfully!")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", "Failed to create lead. Please check the console for details.")
            else:
                error_msg = "Failed to create new person for the lead."
                if new_person_result:
                    error_msg += f"\nError details: {new_person_result}"
                QMessageBox.critical(self, "Error", error_msg)


# --- Leads Page ---
class LeadsPage(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.setObjectName("contentArea")

        self.layout = QVBoxLayout(self)
        self.title = QLabel("Leads Management")
        self.title.setObjectName("page-title")
        self.layout.addWidget(self.title)

        # Search Bar
        self.search_layout = QHBoxLayout()
        self.search_label = QLabel("Search by Name:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter lead name to search...")
        self.search_input.textChanged.connect(self.load_leads)
        self.search_layout.addWidget(self.search_label)
        self.search_layout.addWidget(self.search_input)
        self.layout.addLayout(self.search_layout)

        # Filter and Action Bar
        self.filter_layout = QHBoxLayout()

        # Add Labels for filters and then the filter widgets
        self.filter_layout.addWidget(QLabel("Employee:"))
        self.emp_filter_combo = QComboBox()
        self.emp_filter_combo.addItem("All Employees", None)
        self.filter_layout.addWidget(self.emp_filter_combo)

        self.filter_layout.addWidget(QLabel("Status:"))
        self.status_filter_combo = QComboBox()
        self.status_filter_combo.addItem("All Statuses", None)
        self.filter_layout.addWidget(self.status_filter_combo)

        self.filter_layout.addWidget(QLabel("Start Date:"))
        self.start_date_filter = QDateEdit(calendarPopup=True)
        self.start_date_filter.setDate(QDate(2020, 1, 1))
        self.filter_layout.addWidget(self.start_date_filter)

        self.filter_layout.addWidget(QLabel("End Date:"))
        self.end_date_filter = QDateEdit(calendarPopup=True)
        self.end_date_filter.setDate(QDate.currentDate())
        self.filter_layout.addWidget(self.end_date_filter)

        self.load_filter_dropdowns()

        self.filter_button = QPushButton("Apply Filters")
        self.filter_button.clicked.connect(self.load_leads)

        self.create_lead_button = QPushButton("Create New Lead")
        self.create_lead_button.clicked.connect(self.open_create_lead_dialog)

        self.refresh_button = QPushButton("Refresh Leads")
        self.refresh_button.clicked.connect(self.load_leads)

        self.filter_layout.addWidget(self.filter_button)
        self.filter_layout.addStretch(1)
        self.filter_layout.addWidget(self.create_lead_button)
        self.filter_layout.addWidget(self.refresh_button)
        self.layout.addLayout(self.filter_layout)

        # Action Buttons
        self.action_layout = QHBoxLayout()
        
        # Edit Button
        self.edit_button = QPushButton("Edit Selected Lead")
        self.edit_button.setEnabled(False)  # Initially disabled
        self.edit_button.setVisible(True)   # Ensure visible
        self.edit_button.clicked.connect(self.edit_selected_lead)
        print("Edit button created and connected")  # Debug print
        
        # Delete Button
        self.delete_button = QPushButton("Delete Selected Lead")
        self.delete_button.setEnabled(False)
        self.delete_button.setVisible(True)
        self.delete_button.setProperty("class", "danger")
        self.delete_button.clicked.connect(self.delete_selected_lead)
        print("Delete button created and connected")  # Debug print
        
        # Convert Button
        self.convert_button = QPushButton("Convert to Customer")
        self.convert_button.setEnabled(False)
        self.convert_button.setVisible(True)
        self.convert_button.clicked.connect(self.convert_selected_lead)
        print("Convert button created and connected")  # Debug print
        
        self.action_layout.addWidget(self.edit_button)
        self.action_layout.addWidget(self.delete_button)
        self.action_layout.addWidget(self.convert_button)
        self.layout.addLayout(self.action_layout)

        # Leads Table
        self.leads_table = QTableWidget()
        self.leads_table.setColumnCount(6)
        self.leads_table.setHorizontalHeaderLabels(["ID", "Lead Name", "Assigned Employee", "Status", "Date Created", "Notes"])
        self.leads_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.leads_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.leads_table.setSelectionMode(QTableWidget.SingleSelection)
        self.leads_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.leads_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.layout.addWidget(self.leads_table)

        # Follow-up Checklist Section
        self.followup_section_title = QLabel("Pending Follow-ups")
        self.followup_section_title.setStyleSheet("font-size: 20px; font-weight: bold; margin-top: 20px; margin-bottom: 10px; border-bottom: 1px solid #e0e0e0; padding-bottom: 5px;")
        self.layout.addWidget(self.followup_section_title)

        self.followup_list = QListWidget()
        self.layout.addWidget(self.followup_list)

        self.load_leads()
        self.load_pending_followups()

    def load_filter_dropdowns(self):
        """Load data for filter dropdowns"""
        employees = self.db.getAllEmployees()
        if employees:
            for e in employees:
                self.emp_filter_combo.addItem(e['employeeName'], e['empID'])

        statuses = self.db.getAllStatus()
        if statuses:
            for s in statuses:
                self.status_filter_combo.addItem(s['statusName'], s['statusID'])

    def load_pending_followups(self):
        """Load pending follow-ups"""
        self.followup_list.clear()
        followups = self.db.getPendingFollowUps()
        if followups:
            for fu in followups:
                item_text = f"Lead: {fu['leadID']} - {fu['notes']} (Due: {fu['followUpDate'].strftime('%Y-%m-%d')})"
                item = QListWidgetItem(item_text)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
                item.setData(Qt.UserRole, fu['followUpID'])
                self.followup_list.addItem(item)
            self.followup_list.itemChanged.connect(self.handle_followup_checked)
        else:
            self.followup_list.addItem("No pending follow-ups.")

    def handle_followup_checked(self, item):
        """Handle follow-up completion"""
        if item.checkState() == Qt.Checked:
            follow_up_id = item.data(Qt.UserRole)
            reply = QMessageBox.question(self, "Confirm Completion",
                                         f"Mark follow-up '{item.text()}' as completed?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                success = self.db.completeFollowUp(follow_up_id)
                if success is not None:
                    QMessageBox.information(self, "Success", "Follow-up marked as completed.")
                    self.load_pending_followups()
                else:
                    QMessageBox.critical(self, "Error", "Failed to mark follow-up as completed.")
                    item.setCheckState(Qt.Unchecked)
            else:
                item.setCheckState(Qt.Unchecked)

    def open_create_lead_dialog(self):
        """Open dialog to create a new lead"""
        dialog = LeadFormDialog(self.db, parent=self)
        if dialog.exec() == QDialog.Accepted:
            self.load_leads()
            self.load_pending_followups()

    def on_selection_changed(self):
        """Handle row selection changes"""
        selected_rows = self.leads_table.selectedItems()
        has_selection = len(selected_rows) > 0
        print(f"Selection changed. Has selection: {has_selection}")  # Debug print
        
        # Enable/disable buttons
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
        self.convert_button.setEnabled(has_selection)
        
        # Debug prints for button states
        print(f"Edit button enabled: {self.edit_button.isEnabled()}")
        print(f"Delete button enabled: {self.delete_button.isEnabled()}")
        print(f"Convert button enabled: {self.convert_button.isEnabled()}")

    def get_selected_lead_data(self):
        """Get the data for the currently selected lead"""
        selected_rows = self.leads_table.selectedItems()
        if not selected_rows:
            print("No rows selected")  # Debug print
            return None
        
        row = selected_rows[0].row()
        lead_id = int(self.leads_table.item(row, 0).text())
        print(f"Selected lead ID: {lead_id}")  # Debug print
        
        # Find the lead data from the current leads_data
        for lead in self.current_leads_data:
            if lead['leadID'] == lead_id:
                print(f"Found lead data: {lead}")  # Debug print
                return lead
        print(f"Lead data not found for ID: {lead_id}")  # Debug print
        return None

    def edit_selected_lead(self):
        """Edit the currently selected lead"""
        print("Edit button clicked")  # Debug print
        lead_data = self.get_selected_lead_data()
        if lead_data:
            print(f"Opening edit dialog for lead: {lead_data}")  # Debug print
            dialog = LeadFormDialog(self.db, lead_data=lead_data, parent=self)
            if dialog.exec() == QDialog.Accepted:
                self.load_leads()
        else:
            print("No lead selected for editing")  # Debug print
            QMessageBox.warning(self, "No Selection", "Please select a lead to edit.")

    def delete_selected_lead(self):
        """Delete the currently selected lead"""
        lead_data = self.get_selected_lead_data()
        if lead_data:
            reply = QMessageBox.question(self, "Confirm Delete",
                                     f"Are you sure you want to delete lead '{lead_data['leadName']}' (ID: {lead_data['leadID']})?\n"
                                       "This action cannot be undone!",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                success = self.db.deleteLead(lead_data['leadID'])
                if success:
                    QMessageBox.information(self, "Success", "Lead deleted successfully.")
                    self.load_leads()
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete lead. Please check the console for details.")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a lead to delete.")

    def convert_selected_lead(self):
        """Convert the selected lead to a customer"""
        print("Convert button clicked")  # Debug print
        lead_data = self.get_selected_lead_data()
        if lead_data:
            print(f"Converting lead to customer: {lead_data}")  # Debug print
            if not lead_data.get('personID'):
                QMessageBox.critical(self, "Error", "Cannot convert lead: Person ID is missing.")
                return
                
            reply = QMessageBox.question(self, "Confirm Conversion",
                                       f"Are you sure you want to convert lead '{lead_data['leadName']}' to a customer?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                success = self.db.createCustomer(lead_data['leadID'], lead_data['personID'])
                if success:
                    QMessageBox.information(self, "Success", "Lead converted to customer successfully!")
                    self.load_leads()  # Refresh the leads list
                else:
                    QMessageBox.warning(self, "Conversion Failed", 
                                      "This lead has already been converted to a customer. Each lead can only be converted once.")
        else:
            print("No lead selected for conversion")  # Debug print
            QMessageBox.warning(self, "No Selection", "Please select a lead to convert.")

    def load_leads(self):
        search_text = self.search_input.text().strip().lower()
        emp_id = self.emp_filter_combo.currentData()
        status_id = self.status_filter_combo.currentData()
        start_date = self.start_date_filter.date().toString(Qt.ISODate) if self.start_date_filter.date() != QDate(2020, 1, 1) else None
        end_date = self.end_date_filter.date().toString(Qt.ISODate) if self.end_date_filter.date() != QDate.currentDate() else None

        self.current_leads_data = self.db.getLeads(emp_id, status_id, start_date, end_date)
        self.leads_table.setRowCount(0)

        if self.current_leads_data:
            # Filter by search text if provided
            if search_text:
                self.current_leads_data = [lead for lead in self.current_leads_data if search_text in lead['leadName'].lower()]
            
            self.leads_table.setRowCount(len(self.current_leads_data))
            for row_idx, lead in enumerate(self.current_leads_data):
                # Store the complete lead data
                lead_data = {
                    'leadID': lead['leadID'],
                    'personID': lead['personID'],
                    'leadName': lead['leadName'],
                    'assignedEmployee': lead['assignedEmployee'],
                    'statusName': lead['statusName'],
                    'dateCreated': lead['dateCreated'],
                    'notes': lead.get('notes', ''),
                    'sourceID': lead['sourceID'],
                    'statusID': lead['statusID'],
                    'empID': lead['empID'],
                    'email': lead.get('email', ''),
                    'phone': lead.get('phone', '')
                }
                self.current_leads_data[row_idx] = lead_data

                # Set the table items
                self.leads_table.setItem(row_idx, 0, QTableWidgetItem(str(lead['leadID'])))
                self.leads_table.setItem(row_idx, 1, QTableWidgetItem(lead['leadName']))
                self.leads_table.setItem(row_idx, 2, QTableWidgetItem(lead['assignedEmployee']))
                self.leads_table.setItem(row_idx, 3, QTableWidgetItem(lead['statusName']))
                self.leads_table.setItem(row_idx, 4, QTableWidgetItem(lead['dateCreated'].strftime('%Y-%m-%d %H:%M')))
                self.leads_table.setItem(row_idx, 5, QTableWidgetItem(lead.get('notes', '')))
        else:
            self.leads_table.setRowCount(1)
            self.leads_table.setItem(0, 0, QTableWidgetItem("No leads found."))
            self.leads_table.setSpan(0, 0, 1, 6)


# --- Customer Profile Dialog ---
class CustomerProfileDialog(QDialog):
    def __init__(self, db_manager, customer_id, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.customer_id = customer_id
        self.setWindowTitle(f"Customer Profile (ID: {customer_id})")
        self.setMinimumSize(700, 600)
        self.setStyleSheet(QSS)

        self.layout = QVBoxLayout(self)

        # Add Edit button at the top
        self.edit_button = QPushButton("Edit Customer Details")
        self.edit_button.clicked.connect(self.open_edit_dialog)
        self.layout.addWidget(self.edit_button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        self.load_profile_data()

    def open_edit_dialog(self):
        profile = self.db.getCustomerDetailedProfile(self.customer_id)
        if not profile:
            QMessageBox.warning(self, "Error", "Could not load customer profile for editing.")
            return

        dialog = CustomerEditDialog(self.db, profile, parent=self)
        if dialog.exec() == QDialog.Accepted:
            self.load_profile_data()  # Refresh profile after update

    def add_section_title(self, title):
        title_label = QLabel(title)
        title_label.setProperty("class", "profile-section-title")
        self.scroll_layout.addWidget(title_label)

    def add_info_row(self, label_text, value_text):
        row_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setProperty("class", "profile-info-label")
        value = QLabel(str(value_text))
        value.setProperty("class", "profile-info-value")
        row_layout.addWidget(label)
        row_layout.addWidget(value)
        row_layout.addStretch(1)
        self.scroll_layout.addLayout(row_layout)

    def load_profile_data(self):
        # Clear existing content
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub_item = item.layout().takeAt(0)
                    if sub_item.widget():
                        sub_item.widget().deleteLater()
                item.layout().deleteLater()

        profile = self.db.getCustomerDetailedProfile(self.customer_id)
        if not profile:
            self.scroll_layout.addWidget(QLabel("Customer profile not found."))
            return

        # Header Section
        header_frame = QFrame()
        header_frame.setObjectName("profileHeader")
        header_layout = QVBoxLayout(header_frame)
        header_layout.addWidget(QLabel(f"Name: <span style='font-weight: normal;'>{profile.get('name', 'N/A')}</span>"))
        header_layout.addWidget(QLabel(f"Email: <span style='font-weight: normal;'>{profile.get('email', 'N/A')}</span>"))
        header_layout.addWidget(QLabel(f"Phone: <span style='font-weight: normal;'>{profile.get('phone', 'N/A')}</span>"))
        header_layout.addWidget(QLabel(f"Assigned Employee: <span style='font-weight: normal;'>{profile.get('assignedEmployeeName', 'N/A')} ({profile.get('assignedEmployeeRole', 'N/A')})</span>"))
        header_layout.addWidget(QLabel(f"Campaign Origin: <span style='font-weight: normal;'>{profile.get('campaignName', 'N/A')} ({profile.get('sourceName', 'N/A')})</span>"))
        self.scroll_layout.addWidget(header_frame)

        # Personal Info & Preferences Section
        self.add_section_title("Personal Info & Preferences")
        self.add_info_row("Customer ID:", profile.get('custID'))
        self.add_info_row("Created On:", profile.get('customerCreationDate').strftime('%Y-%m-%d %H:%M') if profile.get('customerCreationDate') else 'N/A')
        self.add_info_row("Last Updated:", profile.get('customerLastUpdated').strftime('%Y-%m-%d %H:%M') if profile.get('customerLastUpdated') else 'N/A')
        self.add_info_row("Preferred Language:", profile.get('preferredLanguage', 'N/A'))
        self.add_info_row("Preferred Contact Time:", profile.get('preferredContactTime', 'N/A'))
        self.add_info_row("Preferred Budget:", f"${profile.get('preferredBudget', 0.0):.2f}")
        self.add_info_row("Preferred Contact Method:", profile.get('preferredContactMethod', 'N/A'))

        # Interactions Section
        self.add_section_title("Interactions History")
        interactions = self.db.getCustomerInteractions(self.customer_id)
        if interactions:
            for interaction in interactions:
                self.scroll_layout.addWidget(QLabel(f"- {interaction['interactionDate'].strftime('%Y-%m-%d %H:%M')} ({interaction['channelName']}): {interaction['notes']} (By: {interaction['employeeRole']})"))
        else:
            self.scroll_layout.addWidget(QLabel("No interaction history."))

        # Product Interests Section
        self.add_section_title("Product Interests")
        product_interests = self.db.getCustomerProductInterests(self.customer_id)
        if product_interests:
            for interest in product_interests:
                self.scroll_layout.addWidget(QLabel(f"- {interest['productName']}"))
        else:
            self.scroll_layout.addWidget(QLabel("No product interests defined."))
        
        add_product_interest_button = QPushButton("Manage Product Interests")
        add_product_interest_button.clicked.connect(self.open_manage_product_interests_dialog)
        self.scroll_layout.addWidget(add_product_interest_button)

        # Status Journey Section
        self.add_section_title("Status Journey")
        status_journey = self.db.getCustomerStatusJourney(self.customer_id)
        if status_journey:
            for status_change in status_journey:
                self.scroll_layout.addWidget(QLabel(f"- {status_change['changeDate'].strftime('%Y-%m-%d %H:%M')}: {status_change['statusName']} (Notes: {status_change['notes']})"))
        else:
            self.scroll_layout.addWidget(QLabel("No status journey history."))

        self.scroll_layout.addStretch(1)

    def open_manage_product_interests_dialog(self):
        dialog = CustomerProductInterestDialog(self.db, self.customer_id, parent=self)
        if dialog.exec() == QDialog.Accepted:
            self.load_profile_data()


# --- Customer Preferences Dialog ---
class CustomerPreferencesDialog(QDialog):
    def __init__(self, db_manager, customer_profile, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.customer_profile = customer_profile
        self.cust_pref_id = customer_profile.get('custPrefID') # May be None if no prefs exist yet
        self.setWindowTitle("Edit Customer Preferences")
        self.setMinimumWidth(350)
        self.setStyleSheet(QSS)

        self.layout = QFormLayout(self)

        self.lang_input = QLineEdit(customer_profile.get('preferredLanguage', ''))
        self.contact_time_input = QLineEdit(customer_profile.get('preferredContactTime', ''))
        self.budget_input = QLineEdit(str(customer_profile.get('preferredBudget', '')))

        self.contact_method_combo = QComboBox()
        self.load_contact_methods()
        self._set_combo_selection(self.contact_method_combo, customer_profile.get('preferredContactMethodID')) # Use preferredContactMethodID from profile


        self.layout.addRow("Language:", self.lang_input)
        self.layout.addRow("Preferred Contact Time:", self.contact_time_input)
        self.layout.addRow("Budget:", self.budget_input)
        self.layout.addRow("Contact Method:", self.contact_method_combo)

        save_button = QPushButton("Save Preferences")
        save_button.clicked.connect(self.save_preferences)
        self.layout.addRow(save_button)

    def _set_combo_selection(self, combo_box, value_id):
        if value_id is None:
            return
        for i in range(combo_box.count()):
            if combo_box.itemData(i) == value_id:
                combo_box.setCurrentIndex(i)
                return

    def load_contact_methods(self):
        methods = self.db.getAllContactMethods()
        if methods:
            self.contact_method_combo.addItem("Select Method", None)
            for m in methods:
                self.contact_method_combo.addItem(m['methodName'], m['methodID'])

    def save_preferences(self):
        contact_method_id = self.contact_method_combo.currentData()
        lang = self.lang_input.text().strip()
        contact_time = self.contact_time_input.text().strip()
        budget_str = self.budget_input.text().strip()

        if not (contact_method_id and lang and contact_time and budget_str):
            QMessageBox.warning(self, "Input Error", "Please fill all preference fields.")
            return

        try:
            budget = float(budget_str)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Budget must be a valid number.")
            return

        # Check if customer_preferences record exists. If not, you'd need to create it first.
        # The current schema for customerPreferences implies a 1-to-1 or 1-to-many relationship
        # where there might be multiple preferences for a customer.
        # For simplicity, we assume cust_pref_id is available from the profile for update.
        if self.cust_pref_id:
            success = self.db.updateCustomerPreferences(
                self.cust_pref_id, contact_method_id, lang, contact_time, budget
            )
            if success is not None:
                QMessageBox.information(self, "Success", "Preferences updated.")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Failed to update preferences.")
        else:
            # If cust_pref_id is None, it means no preferences record exists for this customer.
            # You would need a procedure like `createCustomerPreferences(custID, ...)` here.
            # For this example, we'll show a warning and not proceed.
            QMessageBox.critical(self, "Error", "No existing preferences record found. Cannot update. (Feature to create new preference not implemented yet).")


# --- Customer Product Interest Dialog ---
class CustomerProductInterestDialog(QDialog):
    def __init__(self, db_manager, customer_id, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.customer_id = customer_id
        self.setWindowTitle("Manage Product Interests")
        self.setMinimumWidth(400)
        self.setStyleSheet(QSS)

        self.layout = QVBoxLayout(self)

        self.add_section_title("Current Interests")
        self.current_interests_list = QListWidget()
        self.layout.addWidget(self.current_interests_list)

        self.add_section_title("Add New Interest")
        self.product_combo = QComboBox()
        self.load_products()
        self.add_interest_button = QPushButton("Add Interest")
        self.add_interest_button.clicked.connect(self.add_product_interest)
        
        add_layout = QHBoxLayout()
        add_layout.addWidget(self.product_combo)
        add_layout.addWidget(self.add_interest_button)
        self.layout.addLayout(add_layout)

        self.load_current_interests()

    def add_section_title(self, title):
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-top: 10px; margin-bottom: 5px;")
        self.layout.addWidget(title_label)

    def load_products(self):
        products = self.db.getProducts()
        if products:
            self.product_combo.addItem("Select Product", None)
            for p in products:
                self.product_combo.addItem(p['productName'], p['productID'])

    def load_current_interests(self):
        self.current_interests_list.clear()
        interests = self.db.getCustomerProductInterests(self.customer_id)
        if interests:
            for interest in interests:
                item = QListWidgetItem(interest['productName'])
                item.setData(Qt.UserRole, interest['productID'])
                
                # Create a custom widget for the list item to include a remove button
                widget = QWidget()
                h_layout = QHBoxLayout(widget)
                h_layout.setContentsMargins(0,0,0,0) # Remove padding for compact layout
                
                label = QLabel(interest['productName'])
                h_layout.addWidget(label)
                h_layout.addStretch(1) # Push button to the right

                remove_button = QPushButton("Remove")
                remove_button.setFixedSize(60, 28) # Fixed size for consistency
                remove_button.setProperty("class", "danger") # For QSS styling
                # Use functools.partial or lambda to pass arguments to the slot
                remove_button.clicked.connect(lambda _, prod_id=interest['productID']: self.remove_product_interest(prod_id))
                h_layout.addWidget(remove_button)
                
                self.current_interests_list.addItem(item)
                self.current_interests_list.setItemWidget(item, widget)
        else:
            self.current_interests_list.addItem("No current product interests.")

    def add_product_interest(self):
        product_id = self.product_combo.currentData()
        if product_id is None:
            QMessageBox.warning(self, "Selection Error", "Please select a product to add.")
            return

        success = self.db.addCustomerProductInterest(self.customer_id, product_id)
        if success is not None:
            QMessageBox.information(self, "Success", "Product interest added.")
            self.load_current_interests()
            # self.accept() # Don't close dialog, allow adding multiple
        else:
            QMessageBox.critical(self, "Error", "Failed to add product interest. (Might already be added)")

    def remove_product_interest(self, product_id):
        reply = QMessageBox.question(self, "Confirm Remove",
                                     "Are you sure you want to remove this product interest?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            success = self.db.removeCustomerProductInterest(self.customer_id, product_id)
            if success is not None:
                QMessageBox.information(self, "Success", "Product interest removed.")
                self.load_current_interests()
                # self.accept() # Don't close dialog, allow removing multiple
            else:
                QMessageBox.critical(self, "Error", "Failed to remove product interest.")


# --- Customers Page ---
class CustomersPage(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.setObjectName("contentArea")

        self.layout = QVBoxLayout(self)
        self.title = QLabel("Customers Management")
        self.title.setObjectName("page-title")
        self.layout.addWidget(self.title)

        # Search Bar
        self.search_layout = QHBoxLayout()
        self.search_label = QLabel("Search by Name:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter customer name to search...")
        self.search_input.textChanged.connect(self.load_customers)
        self.search_layout.addWidget(self.search_label)
        self.search_layout.addWidget(self.search_input)
        self.layout.addLayout(self.search_layout)

        # Filter Layout
        self.filter_layout = QHBoxLayout()

        self.filter_layout.addWidget(QLabel("Created From:"))
        self.start_date_filter = QDateEdit(calendarPopup=True)
        self.start_date_filter.setDate(QDate(2020, 1, 1))
        self.filter_layout.addWidget(self.start_date_filter)

        self.filter_layout.addWidget(QLabel("To:"))
        self.end_date_filter = QDateEdit(calendarPopup=True)
        self.end_date_filter.setDate(QDate.currentDate())
        self.filter_layout.addWidget(self.end_date_filter)

        self.filter_layout.addWidget(QLabel("Min Budget:"))
        self.min_budget_filter = QLineEdit()
        self.filter_layout.addWidget(self.min_budget_filter)

        self.filter_layout.addWidget(QLabel("Max Budget:"))
        self.max_budget_filter = QLineEdit()
        self.filter_layout.addWidget(self.max_budget_filter)

        self.filter_layout.addWidget(QLabel("Product Interest:"))
        self.product_interest_combo = QComboBox()
        self.product_interest_combo.addItem("All Products", None)
        self.load_product_filter_dropdown()
        self.filter_layout.addWidget(self.product_interest_combo)

        self.apply_filter_button = QPushButton("Apply Filters")
        self.apply_filter_button.clicked.connect(self.load_customers)

        self.refresh_button = QPushButton("Refresh Customers")
        self.refresh_button.clicked.connect(self.load_customers)

        self.filter_layout.addWidget(self.apply_filter_button)
        self.filter_layout.addStretch(1)
        self.filter_layout.addWidget(self.refresh_button)
        self.layout.addLayout(self.filter_layout)

        # Action Buttons
        self.action_layout = QHBoxLayout()
        
        # Edit Button
        self.edit_button = QPushButton("Edit Selected Customer")
        self.edit_button.clicked.connect(self.edit_selected_customer)
        self.edit_button.setEnabled(False)
        
        # View Button
        self.view_button = QPushButton("View Customer Details")
        self.view_button.clicked.connect(self.view_selected_customer)
        self.view_button.setEnabled(False)
        
        # Delete Button
        self.delete_button = QPushButton("Delete Selected Customer")
        self.delete_button.clicked.connect(self.delete_selected_customer)
        self.delete_button.setEnabled(False)
        self.delete_button.setProperty("class", "danger")
        
        self.action_layout.addWidget(self.edit_button)
        self.action_layout.addWidget(self.view_button)
        self.action_layout.addWidget(self.delete_button)
        self.layout.addLayout(self.action_layout)

        # Customers Table
        self.customers_table = QTableWidget()
        self.customers_table.setColumnCount(5)
        self.customers_table.setHorizontalHeaderLabels(["ID", "Customer Name", "Email", "Phone", "Date Created"])
        self.customers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.customers_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.customers_table.setSelectionMode(QTableWidget.SingleSelection)
        self.customers_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.customers_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.layout.addWidget(self.customers_table)

        self.load_customers()

    def load_product_filter_dropdown(self):
        """Load products into the filter dropdown"""
        products = self.db.getProducts()
        if products:
            for p in products:
                self.product_interest_combo.addItem(p['productName'], p['productID'])

    def on_selection_changed(self):
        """Handle row selection changes"""
        selected_rows = self.customers_table.selectedItems()
        has_selection = len(selected_rows) > 0
        self.edit_button.setEnabled(has_selection)
        self.view_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)

    def get_selected_customer_data(self):
        """Get the data for the currently selected customer"""
        selected_rows = self.customers_table.selectedItems()
        if not selected_rows:
            return None
        
        row = selected_rows[0].row()
        customer_id = int(self.customers_table.item(row, 0).text())
        
        # Find the customer data from the current customers_data
        for customer in self.current_customers_data:
            if customer['custID'] == customer_id:
                return customer
        return None

    def edit_selected_customer(self):
        """Edit the currently selected customer"""
        customer_data = self.get_selected_customer_data()
        if customer_data:
            # Get the full customer profile for editing
            profile = self.db.getCustomerDetailedProfile(customer_data['custID'])
            if profile:
                dialog = CustomerEditDialog(self.db, profile, parent=self)
                if dialog.exec() == QDialog.Accepted:
                    self.load_customers()  # Refresh the customers list
            else:
                QMessageBox.warning(self, "Error", "Could not load customer profile for editing.")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a customer to edit.")

    def view_selected_customer(self):
        """View the currently selected customer's details"""
        customer_data = self.get_selected_customer_data()
        if customer_data:
            self.open_customer_profile(customer_data['custID'])

    def delete_selected_customer(self):
        """Delete the currently selected customer"""
        customer_data = self.get_selected_customer_data()
        if customer_data:
            self.confirm_delete_customer(customer_data['custID'], customer_data['customerName'])

    def load_customers(self):
        search_text = self.search_input.text().strip().lower()
        start_date = self.start_date_filter.date().toString(Qt.ISODate) if self.start_date_filter.date() != QDate(2020, 1, 1) else None
        end_date = self.end_date_filter.date().toString(Qt.ISODate) if self.end_date_filter.date() != QDate.currentDate() else None
        
        # Validate budget inputs
        min_budget = None
        if self.min_budget_filter.text():
            try:
                min_budget = float(self.min_budget_filter.text())
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Minimum budget must be a valid number.")
                return

        max_budget = None
        if self.max_budget_filter.text():
            try:
                max_budget = float(self.max_budget_filter.text())
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Maximum budget must be a valid number.")
                return

        product_id = self.product_interest_combo.currentData()

        self.current_customers_data = self.db.getAllCustomers(start_date, end_date, min_budget, max_budget, product_id)
        self.customers_table.setRowCount(0)

        if self.current_customers_data:
            # Filter by search text if provided
            if search_text:
                self.current_customers_data = [customer for customer in self.current_customers_data if search_text in customer['customerName'].lower()]
            
            self.customers_table.setRowCount(len(self.current_customers_data))
            for row_idx, customer in enumerate(self.current_customers_data):
                self.customers_table.setItem(row_idx, 0, QTableWidgetItem(str(customer['custID'])))
                self.customers_table.setItem(row_idx, 1, QTableWidgetItem(customer['customerName']))
                self.customers_table.setItem(row_idx, 2, QTableWidgetItem(customer['email']))
                self.customers_table.setItem(row_idx, 3, QTableWidgetItem(customer['phone']))
                self.customers_table.setItem(row_idx, 4, QTableWidgetItem(customer['dateCreated'].strftime('%Y-%m-%d %H:%M')))
        else:
            self.customers_table.setRowCount(1)
            self.customers_table.setItem(0, 0, QTableWidgetItem("No customers found."))
            self.customers_table.setSpan(0, 0, 1, 5)

    def open_customer_profile(self, customer_id):
        dialog = CustomerProfileDialog(self.db, customer_id, parent=self)
        dialog.exec()
        self.load_customers()  # Refresh customer list in case preferences/interests changed

    def confirm_delete_customer(self, cust_id, cust_name):
        reply = QMessageBox.question(self, "Confirm Delete",
                                     f"Are you sure you want to delete customer '{cust_name}' (ID: {cust_id})?\n"
                                     "This action cannot be undone and will delete all related data!",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            success = self.db.deleteCustomer(cust_id)
            if success is not None:
                QMessageBox.information(self, "Success", "Customer deleted successfully.")
                self.load_customers()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete customer.")


# --- Main Application Window ---
class CRMApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize DB Manager first, as it's needed for login
        self.db_manager = DatabaseManager(DB_CONFIG)
        # Attempt initial connection for the login dialog
        if not self.db_manager.connect():
            sys.exit(1) # Exit if initial connection fails

        # Show the login dialog
        login_dialog = LoginDialog(self.db_manager)
        if login_dialog.exec() != QDialog.Accepted:
            sys.exit(0) # Exit if login is cancelled or fails

        # If login successful, proceed with main window setup
        self.setWindowTitle("Modern CRM Dashboard")
        self.setGeometry(100, 100, 1200, 800) # Initial window size
        self.setStyleSheet(QSS) # Apply global QSS

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0) # Remove default margins

        # Sidebar
        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(200)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setAlignment(Qt.AlignTop) # Align content to top

        self.logo_label = QLabel("CRM")
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.sidebar_layout.addWidget(self.logo_label)

        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_leads = QPushButton("Leads")
        self.btn_customers = QPushButton("Customers")
        self.btn_campaigns = QPushButton("Campaigns & Sources")
        self.btn_products = QPushButton("Products")
        self.btn_employees = QPushButton("Employees")
        self.btn_followups = QPushButton("Follow-ups")
        self.btn_reports = QPushButton("Reports/Analytics")

        self.sidebar_layout.addWidget(self.btn_dashboard)
        self.sidebar_layout.addWidget(self.btn_leads)
        self.sidebar_layout.addWidget(self.btn_customers)
        self.sidebar_layout.addWidget(self.btn_campaigns)
        self.sidebar_layout.addWidget(self.btn_products)
        self.sidebar_layout.addWidget(self.btn_employees)
        self.sidebar_layout.addWidget(self.btn_followups)
        self.sidebar_layout.addWidget(self.btn_reports)
        self.sidebar_layout.addStretch(1) # Push buttons to top

        self.main_layout.addWidget(self.sidebar)

        # Content Area (Stacked Widget)
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Initialize Pages
        self.dashboard_page = DashboardPage(self.db_manager)
        self.leads_page = LeadsPage(self.db_manager)
        self.customers_page = CustomersPage(self.db_manager)
        self.campaigns_page = CampaignsPage(self.db_manager)
        self.products_page = ProductsPage(self.db_manager)
        self.employees_page = EmployeesPage(self.db_manager)
        self.followups_page = FollowUpsPage(self.db_manager)
        self.reports_page = ReportsPage(self.db_manager)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.leads_page)
        self.stacked_widget.addWidget(self.customers_page)
        self.stacked_widget.addWidget(self.campaigns_page)
        self.stacked_widget.addWidget(self.products_page)
        self.stacked_widget.addWidget(self.employees_page)
        self.stacked_widget.addWidget(self.followups_page)
        self.stacked_widget.addWidget(self.reports_page)

        # Connect Navigation Buttons
        self.btn_dashboard.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.dashboard_page))
        self.btn_leads.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.leads_page))
        self.btn_customers.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.customers_page))
        self.btn_campaigns.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.campaigns_page))
        self.btn_products.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.products_page))
        self.btn_employees.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.employees_page))
        self.btn_followups.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.followups_page))
        self.btn_reports.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.reports_page))

        # Set initial page
        self.stacked_widget.setCurrentWidget(self.dashboard_page)
        self.btn_dashboard.setChecked(True) # Highlight initial active button

        # Ensure only one button is checked at a time
        self.button_group = []
        for btn in [self.btn_dashboard, self.btn_leads, self.btn_customers, self.btn_campaigns,
                    self.btn_products, self.btn_employees, self.btn_followups, self.btn_reports]:
            btn.setCheckable(True)
            btn.clicked.connect(self._update_nav_selection)
            self.button_group.append(btn)

    def _update_nav_selection(self):
        """Updates the checked state of navigation buttons."""
        for btn in self.button_group:
            if btn is self.sender():
                btn.setChecked(True)
            else:
                btn.setChecked(False)

    def closeEvent(self, event):
        """Ensures database connection is closed on application exit."""
        self.db_manager.close()
        event.accept()

class CampaignsPage(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create tab widget
        tabs = QTabWidget()
        
        # Campaigns tab
        campaigns_tab = QWidget()
        campaigns_layout = QVBoxLayout()
        self.campaigns_table = QTableWidget()
        self.campaigns_table.setColumnCount(6)
        self.campaigns_table.setHorizontalHeaderLabels(['ID', 'Name', 'Start Date', 'End Date', 'Budget', 'Total Leads'])
        self.campaigns_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        campaigns_layout.addWidget(self.campaigns_table)
        campaigns_tab.setLayout(campaigns_layout)
        
        # Sources tab
        sources_tab = QWidget()
        sources_layout = QVBoxLayout()
        self.sources_table = QTableWidget()
        self.sources_table.setColumnCount(5)
        self.sources_table.setHorizontalHeaderLabels(['ID', 'Name', 'Description', 'Campaign', 'Campaign ID'])
        self.sources_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        sources_layout.addWidget(self.sources_table)
        sources_tab.setLayout(sources_layout)
        
        # Add tabs to tab widget
        tabs.addTab(campaigns_tab, "Campaigns")
        tabs.addTab(sources_tab, "Sources")
        
        layout.addWidget(tabs)
        self.setLayout(layout)
        
        # Load initial data
        self.load_data()

    def load_data(self):
        try:
            # Load campaigns
            campaigns = self.db.getAllCampaigns()
            self.campaigns_table.setRowCount(len(campaigns))
            for i, campaign in enumerate(campaigns):
                self.campaigns_table.setItem(i, 0, QTableWidgetItem(str(campaign['campaignID'])))
                self.campaigns_table.setItem(i, 1, QTableWidgetItem(campaign['name']))
                self.campaigns_table.setItem(i, 2, QTableWidgetItem(str(campaign['startDate'])))
                self.campaigns_table.setItem(i, 3, QTableWidgetItem(str(campaign['endDate'])))
                self.campaigns_table.setItem(i, 4, QTableWidgetItem(str(campaign['budget'])))
                self.campaigns_table.setItem(i, 5, QTableWidgetItem(str(campaign['totalLeadsGenerated'])))
            
            # Load sources
            sources = self.db.getAllSources()
            self.sources_table.setRowCount(len(sources))
            for i, source in enumerate(sources):
                self.sources_table.setItem(i, 0, QTableWidgetItem(str(source['sourceID'])))
                self.sources_table.setItem(i, 1, QTableWidgetItem(source['sourceName']))
                self.sources_table.setItem(i, 2, QTableWidgetItem(source['sourceDesc']))
                self.sources_table.setItem(i, 3, QTableWidgetItem(source['campaignName'] or 'N/A'))
                self.sources_table.setItem(i, 4, QTableWidgetItem(str(source['campaignID'] or 'N/A')))
                
        except Exception as e:
            print(f"Error loading data: {str(e)}")

class ProductsPage(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Create table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(3)
        self.products_table.setHorizontalHeaderLabels(['ID', 'Name', 'Description'])
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.products_table)
        
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        try:
            products = self.db.getProducts()
            self.products_table.setRowCount(len(products))
            for i, product in enumerate(products):
                self.products_table.setItem(i, 0, QTableWidgetItem(str(product['productID'])))
                self.products_table.setItem(i, 1, QTableWidgetItem(product['productName']))
                self.products_table.setItem(i, 2, QTableWidgetItem(product['productDesc']))
        except Exception as e:
            print(f"Error loading data: {str(e)}")

class EmployeesPage(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Create table
        self.employees_table = QTableWidget()
        self.employees_table.setColumnCount(6)
        self.employees_table.setHorizontalHeaderLabels(['ID', 'Name', 'Email', 'Phone', 'Role', 'Date Hired'])
        self.employees_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.employees_table)
        
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        try:
            employees = self.db.getAllEmployees()
            self.employees_table.setRowCount(len(employees))
            for i, employee in enumerate(employees):
                self.employees_table.setItem(i, 0, QTableWidgetItem(str(employee['empID'])))
                self.employees_table.setItem(i, 1, QTableWidgetItem(employee['employeeName']))
                self.employees_table.setItem(i, 2, QTableWidgetItem(employee['email']))
                self.employees_table.setItem(i, 3, QTableWidgetItem(employee['phone']))
                self.employees_table.setItem(i, 4, QTableWidgetItem(employee['role']))
                self.employees_table.setItem(i, 5, QTableWidgetItem(str(employee['dateHired'])))
        except Exception as e:
            print(f"Error loading data: {str(e)}")

class FollowUpsPage(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Create table
        self.followups_table = QTableWidget()
        self.followups_table.setColumnCount(7)
        self.followups_table.setHorizontalHeaderLabels(['ID', 'Lead', 'Employee', 'Notes', 'Date', 'Completed', 'Lead ID'])
        self.followups_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.followups_table)
        
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        try:
            followups = self.db.getAllFollowUps()
            self.followups_table.setRowCount(len(followups))
            for i, followup in enumerate(followups):
                self.followups_table.setItem(i, 0, QTableWidgetItem(str(followup['followUpID'])))
                self.followups_table.setItem(i, 1, QTableWidgetItem(followup['leadPersonName']))
                self.followups_table.setItem(i, 2, QTableWidgetItem(followup['assignedEmployee']))
                self.followups_table.setItem(i, 3, QTableWidgetItem(followup['notes']))
                self.followups_table.setItem(i, 4, QTableWidgetItem(str(followup['followUpDate'])))
                self.followups_table.setItem(i, 5, QTableWidgetItem('Yes' if followup['completed'] else 'No'))
                self.followups_table.setItem(i, 6, QTableWidgetItem(str(followup['leadID'])))
        except Exception as e:
            print(f"Error loading data: {str(e)}")

class ReportsPage(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Analytics Cards
        analytics_frame = QFrame()
        analytics_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
            QLabel {
                font-size: 14px;
                padding: 10px;
                margin: 5px;
                background-color: #f0f0f0;
                border-radius: 5px;
            }
        """)
        
        analytics_layout = QVBoxLayout()
        
        # Create labels for analytics
        self.total_leads_label = QLabel("Total Leads: 0")
        self.total_customers_label = QLabel("Total Customers: 0")
        self.total_campaigns_label = QLabel("Total Campaigns: 0")
        self.total_employees_label = QLabel("Total Employees: 0")
        self.pending_followups_label = QLabel("Pending Follow-ups: 0")
        
        # Add labels to layout
        analytics_layout.addWidget(self.total_leads_label)
        analytics_layout.addWidget(self.total_customers_label)
        analytics_layout.addWidget(self.total_campaigns_label)
        analytics_layout.addWidget(self.total_employees_label)
        analytics_layout.addWidget(self.pending_followups_label)
        
        analytics_frame.setLayout(analytics_layout)
        layout.addWidget(analytics_frame)
        
        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        try:
            # Get total leads
            leads = self.db.getLeads()
            self.total_leads_label.setText(f"Total Leads: {len(leads)}")
            
            # Get total customers
            customers = self.db.getAllCustomers()
            self.total_customers_label.setText(f"Total Customers: {len(customers)}")
            
            # Get total campaigns
            campaigns = self.db.getAllCampaigns()
            self.total_campaigns_label.setText(f"Total Campaigns: {len(campaigns)}")
            
            # Get total employees
            employees = self.db.getAllEmployees()
            self.total_employees_label.setText(f"Total Employees: {len(employees)}")
            
            # Get pending follow-ups
            followups = self.db.getAllFollowUps()
            pending_followups = sum(1 for f in followups if not f['completed'])
            self.pending_followups_label.setText(f"Pending Follow-ups: {pending_followups}")
            
        except Exception as e:
            print(f"Error loading analytics data: {str(e)}")

class CustomerEditDialog(QDialog):
    def __init__(self, db_manager, customer_profile, parent=None):
        super().__init__(parent)
        self.db = db_manager
        self.customer_profile = customer_profile
        self.cust_id = customer_profile.get('custID')
        self.setWindowTitle("Edit Customer Details")
        self.setMinimumWidth(400)
        self.setStyleSheet(QSS)

        self.layout = QFormLayout(self)

        # Personal Information
        self.name_input = QLineEdit(customer_profile.get('name', ''))
        self.email_input = QLineEdit(customer_profile.get('email', ''))
        self.phone_input = QLineEdit(customer_profile.get('phone', ''))

        # Preferences
        self.lang_input = QLineEdit(customer_profile.get('preferredLanguage', ''))
        self.contact_time_input = QLineEdit(customer_profile.get('preferredContactTime', ''))
        self.budget_input = QLineEdit(str(customer_profile.get('preferredBudget', '0.0')))

        # Contact Method Dropdown
        self.contact_method_combo = QComboBox()
        self.load_contact_methods()
        self._set_combo_selection(self.contact_method_combo, customer_profile.get('preferredContactMethodID'))

        # Add fields to layout
        self.layout.addRow("Name:", self.name_input)
        self.layout.addRow("Email:", self.email_input)
        self.layout.addRow("Phone:", self.phone_input)
        self.layout.addRow("Preferred Language:", self.lang_input)
        self.layout.addRow("Preferred Contact Time:", self.contact_time_input)
        self.layout.addRow("Budget:", self.budget_input)
        self.layout.addRow("Contact Method:", self.contact_method_combo)

        # Save button
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_changes)
        self.layout.addRow(save_button)

    def _set_combo_selection(self, combo_box, value_id):
        if value_id is None:
            return
        for i in range(combo_box.count()):
            if combo_box.itemData(i) == value_id:
                combo_box.setCurrentIndex(i)
                return

    def load_contact_methods(self):
        methods = self.db.getAllContactMethods()
        if methods:
            self.contact_method_combo.addItem("Select Method", None)
            for m in methods:
                self.contact_method_combo.addItem(m['methodName'], m['methodID'])

    def save_changes(self):
        print("Starting save_changes method...")  # Debug print
        try:
            # Get all values first
            print("Getting customer profile values...")  # Debug print
            person_id = self.customer_profile.get('personID')
            name = self.name_input.text().strip()
            email = self.email_input.text().strip()
            phone = self.phone_input.text().strip()
            contact_method_id = self.contact_method_combo.currentData()
            lang = self.lang_input.text().strip()
            contact_time = self.contact_time_input.text().strip()
            budget = float(self.budget_input.text() or 0)
            cust_pref_id = self.customer_profile.get('custPrefID')

            print(f"Debug - Values to update:")
            print(f"Person ID: {person_id}")
            print(f"Name: {name}")
            print(f"Email: {email}")
            print(f"Phone: {phone}")
            print(f"Contact Method ID: {contact_method_id}")
            print(f"Language: {lang}")
            print(f"Contact Time: {contact_time}")
            print(f"Budget: {budget}")
            print(f"Customer Preference ID: {cust_pref_id}")

            if not person_id:
                print("Error: Person ID is missing")  # Debug print
                raise Exception("Person ID is missing from customer profile")

            # First update person details
            print("Attempting to update person details...")  # Debug print
            try:
                person_result = self.db.updatePerson(person_id, name, email, phone)
                print(f"Person update result: {person_result}")  # Debug print
            except Exception as e:
                print(f"Error in updatePerson: {str(e)}")  # Debug print
                raise Exception(f"Failed to update person details: {str(e)}")
            
            if not person_result:
                print("Error: Person update returned None")  # Debug print
                raise Exception("Failed to update person details")

            # Then update customer preferences
            if cust_pref_id:
                print("Attempting to update customer preferences...")  # Debug print
                try:
                    pref_result = self.db.updateCustomerPreferences(
                        cust_pref_id,
                        contact_method_id,
                        lang,
                        contact_time,
                        budget
                    )
                    print(f"Preferences update result: {pref_result}")  # Debug print
                except Exception as e:
                    print(f"Error in updateCustomerPreferences: {str(e)}")  # Debug print
                    raise Exception(f"Failed to update customer preferences: {str(e)}")
                
                if not pref_result:
                    print("Error: Preferences update returned None")  # Debug print
                    raise Exception("Failed to update customer preferences")
            else:
                print("Warning: No customer preferences ID found, skipping preferences update")
            
            print("All updates completed successfully")  # Debug print
            QMessageBox.information(self, "Success", "Customer details updated successfully!")
            self.accept()
            
        except ValueError as ve:
            print(f"Value Error caught: {str(ve)}")  # Debug print
            QMessageBox.critical(self, "Input Error", f"Invalid input value: {str(ve)}")
        except Exception as e:
            print(f"General Exception caught: {str(e)}")  # Debug print
            print(f"Error type: {type(e)}")  # Debug print
            import traceback
            print(f"Traceback: {traceback.format_exc()}")  # Debug print
            QMessageBox.critical(self, "Error", f"Failed to update customer details: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS) # Apply QSS globally

    window = CRMApp()
    window.showMaximized() # Start maximized for a better experience
    sys.exit(app.exec())
