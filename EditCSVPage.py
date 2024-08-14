from PyQt5.QtWidgets import QApplication , QSizePolicy, QSpacerItem, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator
from csv_to_DB import csv_to_DB
from UploadCSVPage import UploadCSVPage
import os
from mysql.connector import MySQLConnection
import mysql.connector

class EditCSVPage(QtWidgets.QMainWindow):
    backPressed = pyqtSignal()

    def __init__(self):
        super().__init__()
        #self.shared_data = shared_data  # Store the reference to shared_data
        
        self.line_edit_q_id = None
        self.line_edit_question = None
        self.line_edit_level = None
        self.line_edit_answer = None
        
        self.label_q_id = None
        self.label_question = None
        self.label_level = None
        self.label_answer = None
        
        self.config = {
            "host" :"localhost",
            "user": "root",
            "password" : "new_password",
            "database": "testSqlDb"
        }

            
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor()
        self.cell_item = None
        
        self.setupUi(self)
        self.display_csv()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Edit .csv File")
        MainWindow.resize(885, 638)
        MainWindow.setMinimumSize(QtCore.QSize(885, 638))
        self.fileName = ""

        #Background
        self.background_widget = QtWidgets.QWidget()
        self.background_widget.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0.0113636, x2:1, y2:1, stop:0 rgba(9, 28, 83, 255), stop:1 rgba(138, 41, 115, 255))")
        self.background_widget.setObjectName("background_widget")

        vbox_main = QtWidgets.QVBoxLayout(self.background_widget)
        hbox_buttons = QtWidgets.QHBoxLayout()

        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)

        # Heading
        self.admin_label = QtWidgets.QLabel("Edit .csv File", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(36)
        self.admin_label.setFont(font)
        self.admin_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.admin_label.setAlignment(QtCore.Qt.AlignCenter)
        vbox_main.addWidget(self.admin_label)

        spacer_item = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)


        #Delete CSV Button
        self.deleteButton = QtWidgets.QPushButton("Delete CSV", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        self.deleteButton.setFont(font)
        self.deleteButton.setStyleSheet("""
                                            QPushButton {
                                                background-color: rgb(85, 142, 255);
                                                border: none;
                                                color: rgb(255, 255, 255);
                                                border-radius: 10px;
                                                padding: 5px;
                                            }
                                            QPushButton:hover {
                                                background-color: rgb(55, 112, 225);
                                            }
                                                
                                            QPushButton:pressed {
                                                background-color: rgb(35, 82, 205);
                                            }
                                            
                                            QPushButton:disabled {
                                                background-color: rgb(169, 169, 169); /* Grey background when disabled */
                                                color: rgb(255, 255, 255);
                                            }
                                            
                                        """)
        
        #vbox_main.addWidget(self.deleteButton)
        self.deleteButton.hide()
        self.deleteButton.clicked.connect(self.confrim)

        
        # Create and configure the QTableWidget
        self.tableWidget = QtWidgets.QTableWidget(self.background_widget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)  # Set the number of columns as needed

        # Set the table headers
        self.tableWidget.setHorizontalHeaderLabels(['QuestionID', 'Question', 'Answer', 'Level'])
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(12)
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet("border: 2px solid #FFFFFF;"
                                     "background-color: rgba(0, 0, 0, 0);")
        
        vbox_main.addWidget(self.tableWidget)

        size_policy = self.tableWidget.sizePolicy()
        size_policy.setVerticalPolicy(QSizePolicy.Expanding)
        size_policy.setVerticalStretch(1)
        self.tableWidget.setSizePolicy(size_policy)

        spacer_item = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)
        
        self.tableWidget.cellChanged.connect(self.cell_changed)

        
        #Save Button for delete rows 
        self.saveButton = QtWidgets.QPushButton("Save", self.background_widget)
        self.saveButton.setEnabled(False)


        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        self.saveButton.setFont(font)


        self.saveButton.setStyleSheet("""
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
                                        
                                QPushButton:pressed {
                                    background-color: rgb(37, 148, 70);
                                }
                                """)

        #vbox_main.addWidget(self.submitButton)
        #self.submitButton.hide()
        self.saveButton.clicked.connect(self.save_csv)
        
        #Submit Button for add rows 
        self.submitButton = QtWidgets.QPushButton("Save", self.background_widget)
        self.submitButton.setEnabled(False)


        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        self.submitButton.setFont(font)


        self.submitButton.setStyleSheet("""
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
                                        
                                QPushButton:pressed {
                                    background-color: rgb(37, 148, 70);
                                }
                                """)

        #vbox_main.addWidget(self.submitButton)
        #self.submitButton.hide()
        self.submitButton.clicked.connect(self.submit_csv)

        # Edit Button
        self.edit_button = QtWidgets.QPushButton("Edit Row", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        self.edit_button.setFont(font)
        self.edit_button.setStyleSheet("""
                                            QPushButton {
                                                background-color: rgb(85, 142, 255);
                                                border: none;
                                                color: rgb(255, 255, 255);
                                                border-radius: 10px;
                                                padding: 5px;
                                            }
                                            QPushButton:hover {
                                                background-color: rgb(55, 112, 225);
                                            }
                                                
                                            QPushButton:pressed {
                                                background-color: rgb(35, 82, 205);
                                            }
                                        """)
        
        #vbox_main.addWidget(self.edit_button)
        self.edit_button.clicked.connect(self.edit_csv)
        
        # Delete Row Button
        self.deleteRow_button = QtWidgets.QPushButton("Delete Row", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        self.deleteRow_button.setFont(font)
        self.deleteRow_button.setStyleSheet("""
                                            QPushButton {
                                                background-color: rgb(85, 142, 255);
                                                border: none;
                                                color: rgb(255, 255, 255);
                                                border-radius: 10px;
                                                padding: 5px;
                                            }
                                            QPushButton:hover {
                                                background-color: rgb(55, 112, 225);
                                            }
                                                
                                            QPushButton:pressed {
                                                background-color: rgb(35, 82, 205);
                                            }
                                            
                                            QPushButton:disabled {
                                            background-color: rgb(169, 169, 169); /* Grey background when disabled */
                                            color: rgb(255, 255, 255);
                                            }
                                            
                                        """)
        
        #vbox_main.addWidget(self.deleteRow_button)
        #self.deleteRow_button.hide()
        self.deleteRow_button.clicked.connect(self.delete_row)
        
        #Add Row Button
    
        self.addRow_button = QtWidgets.QPushButton("Add Row", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        self.addRow_button.setFont(font)
        self.addRow_button.setStyleSheet("""
                                            QPushButton {
                                                background-color: rgb(85, 142, 255);
                                                border: none;
                                                color: rgb(255, 255, 255);
                                                border-radius: 10px;
                                                padding: 5px;
                                            }
                                            QPushButton:hover {
                                                background-color: rgb(55, 112, 225);
                                            }
                                                
                                            QPushButton:pressed {
                                                background-color: rgb(35, 82, 205);
                                            }
                                            QPushButton:disabled {
                                            background-color: rgb(169, 169, 169); /* Grey background when disabled */
                                            color: rgb(255, 255, 255);
                                        }
                                        """)
        
        #vbox_main.addWidget(self.addRow_button)
        #self.addRow_button.hide()
        self.addRow_button.clicked.connect(self.add_rows)

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
        
        
        
        
        self.backButton.clicked.connect(self.back)

        MainWindow.setCentralWidget(self.background_widget)

        button_width = 200  # define the desired width of the buttons
        button_width_back = 105
        
        #Assessment ID label
        # self.create_label('index', "Enter QuestionID")
        # vbox_main.addWidget(self.index, 0, QtCore.Qt.AlignCenter)

        #Assessment ID Line Edit
        # self.create_line_edit('qID_input')
        # vbox_main.addWidget(self.qID_input, 0, QtCore.Qt.AlignCenter)
        # self.qID_input.returnPressed.connect(self.enter)
        
        

        # Edit Button
        hbox_edit_button = QHBoxLayout()
        hbox_edit_button.addStretch(1)
        self.edit_button.setFixedWidth(button_width)
        hbox_edit_button.addWidget(self.edit_button)
        hbox_edit_button.addStretch(1)
        vbox_main.addLayout(hbox_edit_button)
        
        # Add Button
        hbox_add_Button = QHBoxLayout()
        hbox_add_Button.addStretch(1)
        self.addRow_button.setFixedWidth(button_width)
        hbox_add_Button.addWidget(self.addRow_button)
        hbox_add_Button.addStretch(1)
        vbox_main.addLayout(hbox_add_Button)

        # Delete Row Button
        hbox_delete_button = QHBoxLayout()
        hbox_delete_button.addStretch(1)
        self.deleteRow_button.setFixedWidth(button_width)
        hbox_delete_button.addWidget(self.deleteRow_button)
        hbox_delete_button.addStretch(1)
        vbox_main.addLayout(hbox_delete_button)

        # Delete Button
        hbox_deleteButton = QHBoxLayout()
        hbox_deleteButton.addStretch(1)
        self.deleteButton.setFixedWidth(button_width)
        hbox_deleteButton.addWidget(self.deleteButton)
        hbox_deleteButton.addStretch(1)
        vbox_main.addLayout(hbox_deleteButton)
        

        # Submit addtions Button
        hbox_submitButton = QHBoxLayout()
        hbox_submitButton.addStretch(1)
        self.submitButton.setFixedWidth(button_width)
        hbox_submitButton.addWidget(self.submitButton)
        hbox_submitButton.addStretch(1)
        vbox_main.addLayout(hbox_submitButton)
        
         # Save deletions Button
        hbox_saveButton = QHBoxLayout()
        hbox_saveButton.addStretch(1)
        self.saveButton.setFixedWidth(button_width)
        hbox_saveButton.addWidget(self.saveButton)
        hbox_saveButton.addStretch(1)
        vbox_main.addLayout(hbox_submitButton)

        hbox_buttons.addWidget(self.edit_button)
        hbox_buttons.addWidget(self.addRow_button)
        hbox_buttons.addWidget(self.deleteRow_button)
        hbox_buttons.addWidget(self.deleteButton)
        hbox_buttons.addWidget(self.submitButton)
        hbox_buttons.addWidget(self.saveButton)
        
        spacer_item = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)

        # Logout Button
        hbox_backButton = QHBoxLayout()
        hbox_backButton.addStretch(1)
        self.backButton.setFixedWidth(button_width_back)
        hbox_backButton.addWidget(self.backButton)
        hbox_backButton.addStretch(1)
        vbox_main.addLayout(hbox_backButton)
        
        hbox_backButton = QHBoxLayout()
        hbox_backButton.addStretch(1)
        self.backButton.setFixedWidth(button_width)
        hbox_backButton.addWidget(self.backButton)
        hbox_backButton.addStretch(1)
        vbox_main.addLayout(hbox_submitButton)
        
        # Create labels and line edits for q_id, question, answer, level
        self.label_q_id = QtWidgets.QLabel("Question ID:", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(12)
        self.label_q_id.setFont(font)
        self.label_q_id.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.label_q_id.setAlignment(QtCore.Qt.AlignCenter)
        #vbox_main.addWidget(self.admin_label)
        
        self.label_question = QtWidgets.QLabel("Question:", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(12)
        self.label_question.setFont(font)
        self.label_question.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.label_question.setAlignment(QtCore.Qt.AlignCenter)
        #vbox_main.addWidget(self.admin_label)
        
        self.label_answer = QtWidgets.QLabel("Answer:", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(12)
        self.label_answer.setFont(font)
        self.label_answer.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.label_answer.setAlignment(QtCore.Qt.AlignCenter)
        #vbox_main.addWidget(self.admin_label)
        
        self.label_level = QtWidgets.QLabel("Level:", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(12)
        self.label_level.setFont(font)
        self.label_level.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.label_level.setAlignment(QtCore.Qt.AlignCenter)
        #vbox_main.addWidget(self.admin_label)

        self.line_edit_q_id = QtWidgets.QLineEdit(self.background_widget)
        int_validator = QIntValidator(self)
        
        self.line_edit_question = QtWidgets.QLineEdit(self.background_widget)
        self.line_edit_answer = QtWidgets.QLineEdit(self.background_widget)
        self.line_edit_level = QtWidgets.QLineEdit(self.background_widget)
        self.line_edit_level.setValidator(int_validator)
        
        self.line_edit_q_id.hide()
        self.line_edit_question.hide()
        self.line_edit_level.hide()
        self.line_edit_answer.hide()
        
        self.label_q_id.hide()
        self.label_question.hide()
        self.label_level.hide()
        self.label_answer.hide()
        
        self.submitButton.hide()
        self.saveButton.hide()

        # Create a horizontal layout for the labels and line edits
        hbox_labels_lineedits = QtWidgets.QHBoxLayout()
        hbox_labels_lineedits.addWidget(self.label_q_id)
        hbox_labels_lineedits.addWidget(self.line_edit_q_id)
        hbox_labels_lineedits.addWidget(self.label_question)
        hbox_labels_lineedits.addWidget(self.line_edit_question)
        hbox_labels_lineedits.addWidget(self.label_answer)
        hbox_labels_lineedits.addWidget(self.line_edit_answer)
        hbox_labels_lineedits.addWidget(self.label_level)
        hbox_labels_lineedits.addWidget(self.line_edit_level)

        # Add the horizontal layout to the main vertical layout (vbox_main) above hbox_buttons
        vbox_main.addLayout(hbox_labels_lineedits)
        vbox_main.addLayout(hbox_buttons)  # Add hbox_buttons below the labels and line edits
        vbox_main.addLayout(hbox_backButton)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
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

    def display_csv(self):
        
        query = "SELECT id, question, answer, level FROM qnaforclassicmodels GROUP BY id, question, answer, level;"  
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.connection.close()
        
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['QuestionID', 'Question', 'Answer', 'Level'])
        
        for row, d in enumerate(result):
            for column, item in enumerate(d):
                 self.cell_item = QTableWidgetItem(str(item))
                # Set the item as read-only
                 self.cell_item.setFlags(self.cell_item.flags() ^ QtCore.Qt.ItemIsEditable)
                 self.tableWidget.setItem(row, column, self.cell_item)
                #self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
  
    def back(self):
        self.backPressed.emit()
        self.close()

    def edit_csv(self):
        for row in range(self.tableWidget.rowCount()):
            for column in range(self.tableWidget.columnCount()):
                cell_flags = self.tableWidget.item(row, column).flags()
                # Remove the read-only flag (Qt.ItemIsEditable) to make the cell editable
                self.tableWidget.item(row, column).setFlags(cell_flags | QtCore.Qt.ItemIsEditable)
                
        self.deleteButton.show()
        self.deleteRow_button.show()
        self.submitButton.show()
        self.addRow_button.show()
        self.edit_button.hide()

    def add_rows(self):
        self.deleteRow_button.hide()
        self.edit_button.hide()
        self.submitButton.show()
        self.addRow_button.setDisabled(True)
      
        self.line_edit_question.show()
        self.line_edit_level.show()
        self.line_edit_answer.show()
        
        
        self.label_question.show()
        self.label_level.show()
        self.label_answer.show()
        
        self.submitButton.setEnabled(True)
    
        
        
    def submit_csv(self):
        self.submitButton.setEnabled(False)
        self.line_edit_q_id.hide()
        self.line_edit_question.hide()
        self.line_edit_level.hide()
        self.line_edit_answer.hide()
        
        self.label_q_id.hide()
        self.label_question.hide()
        self.label_level.hide()
        self.label_answer.hide()
        
        row_position = self.tableWidget.rowCount()
        
        
        data = [row_position, self.line_edit_question.text(), self.line_edit_answer.text(), int(self.line_edit_level.text())]
        
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        
        for column, value in enumerate(data):
            item = QTableWidgetItem(str(value))
            self.tableWidget.setItem(row_position, column, item)
            
        data = (row_position, self.line_edit_question.text(), self.line_edit_answer.text(), int(self.line_edit_level.text()))
            
         #Insert the new row into the database table
        query = "INSERT INTO qnaforclassicmodels (id, question, answer, level) VALUES (%s, %s, %s, %s)"
        
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor()
        
        self.cursor.execute(query, data)  # Execute the query with the data
        self.connection.commit()  # Commit the changes to the database
        self.connection.close()
        self.line_edit_question.clear()
        self.line_edit_answer.clear()
        self.line_edit_level.clear()
        self.addRow_button.setDisabled(False)
            
    
    def delete_row(self):
        self.saveButton.show()
        self.saveButton.setEnabled(True)
        self.addRow_button.hide()
        self.edit_button.hide()
        self.deleteButton.show()
        self.deleteRow_button.setDisabled(True)
        
        self.line_edit_q_id.show()
        self.label_q_id.show()
        
    def confrim(self):
        self.submitButton.setEnabled(True)
        
        msg = QMessageBox()
        msg.setWindowTitle("Confirm")
        msg.setText("Are you sure you want to delete the entire table?")
        msg.setIcon(QMessageBox.Warning)
        msg.addButton(QMessageBox.Yes)
        msg.addButton(QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        
        yes_button = msg.button(QMessageBox.Yes)
        yes_button.clicked.connect(self.delete_csv)
        
        msg.exec_()
    
    def save_csv(self):
        
        index = int(self.line_edit_q_id.text())
        self.tableWidget.removeRow(index)
        
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor()
        
        # Execute a DELETE query to remove the row from the database
        delete_query = "DELETE FROM qnaforclassicmodels WHERE id = %s"
        self.cursor.execute(delete_query, (index,))
        self.connection.close()
        self.line_edit_q_id.clear()
        self.saveButton.setEnabled(False)
        self.deleteRow_button.setEnabled(True)
        
        
    def delete_csv(self):
        
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor()
        truncate_query = "TRUNCATE TABLE qnaforclassicmodels"
        self.cursor.execute(truncate_query)
        
        self.deleteButton.setDisabled(True)
        self.deleteRow_button.setDisabled(True)
        self.saveButton.setDisabled(True)
        
    def cell_changed(self, row, column):
        
        
        # Get the edited value from the cell
        edited_value = self.tableWidget.item(row, column).text()
        
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor()
        
        # Determine which column was edited (e.g., based on column index)
        if column == 1:  
            # Construct an SQL update query to update the database
            query = "UPDATE qnaforclassicmodels SET question = %s WHERE id = %s"
            data = (edited_value, self.tableWidget.item(row, 0).text())  
            
            # Execute the SQL query to update the database
            self.cursor.execute(query, data)
            self.connection.commit()
        elif column == 2:  
            # Construct an SQL update query to update the database
            query = "UPDATE qnaforclassicmodels SET answer = %s WHERE id = %s"
            data = (edited_value, self.tableWidget.item(row, 0).text())  
            
            # Execute the SQL query to update the database
            self.cursor.execute(query, data)
            self.connection.commit()
            
        elif column == 3:
            query = "UPDATE qnaforclassicmodels SET level = %s WHERE id = %s"
            data = (edited_value, self.tableWidget.item(row, 0).text())  
            
            # Execute the SQL query to update the database
            self.cursor.execute(query, data)
            self.connection.commit()