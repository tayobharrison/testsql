from PyQt5.QtWidgets import QApplication, QSizePolicy, QSpacerItem, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from mysql.connector import MySQLConnection
import mysql.connector

class SetAssessmentPage(QtWidgets.QMainWindow):
    backPressed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Set Assessment")
        MainWindow.resize(885, 638)
        MainWindow.setMinimumSize(QtCore.QSize(885, 638))

        #Background
        self.background_widget = QtWidgets.QWidget()
        self.background_widget.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0.0113636, x2:1, y2:1, stop:0 rgba(9, 28, 83, 255), stop:1 rgba(138, 41, 115, 255))")
        self.background_widget.setObjectName("background_widget")
        
        vbox_main = QVBoxLayout(self.background_widget)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)


        # Heading
        self.admin_label = QtWidgets.QLabel("Set Assessment", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(36)
        self.admin_label.setFont(font)
        self.admin_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.admin_label.setAlignment(QtCore.Qt.AlignCenter)
        vbox_main.addWidget(self.admin_label)

        spacer_item = QSpacerItem(10, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)



       # Level 1 label
        self.create_label('level1_label', "Number of Level 1 Questions:")
        vbox_main.addWidget(self.level1_label, 0, QtCore.Qt.AlignCenter)

        # Text edit level 1 input
        self.create_line_edit('level1_input')
        vbox_main.addWidget(self.level1_input, 0, QtCore.Qt.AlignCenter)

        spacer_bottom = QSpacerItem(5, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_bottom)


       # Level 2 label
        self.create_label('level2_label', "Number of Level 2 Questions:")
        vbox_main.addWidget(self.level2_label, 0, QtCore.Qt.AlignCenter)

        # Text edit level 2 input
        self.create_line_edit('level2_input')
        vbox_main.addWidget(self.level2_input, 0, QtCore.Qt.AlignCenter)

        spacer_bottom = QSpacerItem(5, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_bottom)


       # Level 3 label
        self.create_label('level3_label', "Number of Level 3 Questions:")
        vbox_main.addWidget(self.level3_label, 0, QtCore.Qt.AlignCenter)

        # Text edit level 3 input
        self.create_line_edit('level3_input')
        vbox_main.addWidget(self.level3_input, 0, QtCore.Qt.AlignCenter)

        spacer_bottom = QSpacerItem(5, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_bottom)


        # Assessment Code label
        self.create_label('code_label', "Assessment Code:")
        vbox_main.addWidget(self.code_label, 0, QtCore.Qt.AlignCenter)

        # Assessment Code Input
        self.create_line_edit('code_input')
        vbox_main.addWidget(self.code_input, 0, QtCore.Qt.AlignCenter)
        #self.code_input.setPlaceholderText('Number of Level 3 Questions:')

        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_bottom)

        # Create Button
        self.create_button = QtWidgets.QPushButton("Create Assessment", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        self.create_button.setFont(font)
        self.create_button.setStyleSheet("""
                                QPushButton {
                                    background-color: rgb(87, 198, 120);
                                    color: rgb(255, 255, 255);
                                    border-radius: 10px;
                                    padding: 5px;
                                }
                                         
                                QPushButton:disabled {
                                    background-color: rgb(169, 169, 169); /* Grey background when disabled */
                                    color: rgb(255, 255, 255);
                                }
                                QPushButton:hover {
                                    background-color: rgb(57, 168, 90); 
                                    color: rgb(255, 255, 255);
                                }
                                       
                                QPushButton:pressed{
                                    background-color: rgb(37, 148, 70);
                                }
                                """)
        
        vbox_main.addWidget(self.create_button)
        self.create_button.clicked.connect(self.create_assessment)
        self.create_button.setEnabled(False)
        

        #Back Button
        self.backButton = QtWidgets.QPushButton("Back", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(15)
        self.backButton.setFont(font)
        self.backButton.setStyleSheet("""
                                            QPushButton {
                                                background-color: rgb(241, 0, 138);
                                                border: none;
                                                color: rgb(255, 255, 255);
                                                border-radius: 10px;
                                                padding: 4px;
                                            }
                                            QPushButton:hover {
                                                background-color: rgb(191, 0, 108);
                                            }

                                            QPushButton:pressed{
                                                background-color: rgb(171, 0, 88);
                                            }
                                        """)
        
        vbox_main.addWidget(self.backButton)
        self.backButton.clicked.connect(self.back)
        
        MainWindow.setCentralWidget(self.background_widget)  # Set background_widget as the central widget

        button_width = 200
        button_width_back = 105

        self.level1_input.textChanged.connect(self.update_create_button_state)
        self.level2_input.textChanged.connect(self.update_create_button_state)
        self.level3_input.textChanged.connect(self.update_create_button_state)
        self.code_input.textChanged.connect(self.update_create_button_state)
        
        self.create_button.clicked.connect(self.clear_text_fields)


        #Create Button
        hbox_create_button = QHBoxLayout()
        hbox_create_button.addStretch(1)
        self.create_button.setFixedWidth(button_width)
        hbox_create_button.addWidget(self.create_button)
        hbox_create_button.addStretch(1)
        vbox_main.addLayout(hbox_create_button)

        #Back Button
        hbox_backButton = QHBoxLayout()
        hbox_backButton.addStretch(1)
        self.backButton.setFixedWidth(button_width_back)
        hbox_backButton.addWidget(self.backButton)
        hbox_backButton.addStretch(1)
        vbox_main.addLayout(hbox_backButton)
        
    @pyqtSlot()
    
    def update_create_button_state(self):
        # Enable the button if there is text in all input fields, otherwise disable it
        enable_button = bool(self.level1_input.text() and
                            self.level2_input.text() and
                            self.level3_input.text() and
                            self.code_input.text())
        self.create_button.setEnabled(enable_button)

    @pyqtSlot()
    def clear_text_fields(self):
        # Clear all text fields when the button is clicked
        self.level1_input.clear()
        self.level2_input.clear()
        self.level3_input.clear()
        self.code_input.clear()

    def create_assessment(self):
        
        try:
            # Retrieve the number of questions for each level, and the assessment code
            level1_questions = int(self.level1_input.text())
            level2_questions = int(self.level2_input.text())
            level3_questions = int(self.level3_input.text())
            assessment_code = self.code_input.text()

            # assess = Assessment()
            # assess.createAssessment(level1_questions, level2_questions, level3_questions, assessment_code)
            
            
            # Database connection details
            config = {
                "host": "localhost",
                "user": "root",
                "password": "new_password",
                "database": "admin"
            }

            try:
                # Establish a connection
                connection = mysql.connector.connect(**config)
                cursor = connection.cursor()

                create_table_query = """
                    CREATE TABLE IF NOT EXISTS assessments (
                        assessment_code VARCHAR(45) PRIMARY KEY,
                        level1 INT,
                        level2 INT,
                        level3 INT
                    )
                    """
                cursor.execute(create_table_query)

                # Insert the data
                query = "INSERT INTO assessments (assessment_code, level1, level2, level3) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (assessment_code, level1_questions, level2_questions, level3_questions))

                # Commit the changes
                connection.commit()

            except mysql.connector.Error as err:
                # Handle database-related errors
                print(f"An error occurred: {err}")
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText(f"An error occurred while creating the assessment: {err}")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()

            except Exception as e:
                # Handle other exceptions
                print(f"An unexpected error occurred: {e}")
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText(f"An unexpected error occurred: {e}")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()

            finally:
                # Close the cursor and connection, if they were created
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

            # Show a success dialog
            msg = QMessageBox()
            msg.setWindowTitle("Assessment Created")
            msg.setText("The assessment has been successfully created!")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            
        except ValueError:
            # If conversion fails, display error message
            msg = QMessageBox()
            msg.setWindowTitle("Input Error")
            msg.setText("Only numbers can be input for question level.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
    
    def create_line_edit(self, name, read_only=False):
        line_edit = QtWidgets.QLineEdit(self.background_widget)
        line_edit.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
                                "font: 14pt \"Avenir Next\";\n"
                                "color: rgb(160, 186, 255)")
        line_edit.setObjectName(name)
        line_edit.setReadOnly(read_only)
        setattr(self, name, line_edit)

    def create_label(self, name, text, font_size=18):
        label = QtWidgets.QLabel(self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        font.setPointSize(font_size)
        label.setFont(font)
        label.setObjectName(name)
        label.setText(text)
        setattr(self, name, label)

    def back(self):
        self.backPressed.emit()
        self.close()
