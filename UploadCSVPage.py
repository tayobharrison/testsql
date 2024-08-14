from PyQt5.QtWidgets import QApplication, QSizePolicy, QSpacerItem, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from csv_to_DB import csv_to_DB
import sys
from QGen import QGen

class UploadCSVPage(QtWidgets.QMainWindow):
    backPressed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.fileName = None
        self.shared_data = {"fileName": None}  # Initialize shared_data with None
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Upload")
        MainWindow.resize(885, 638)
        MainWindow.setMinimumSize(QtCore.QSize(885, 638))
        self.fileName = ""

        #Background
        self.background_widget = QtWidgets.QWidget()
        self.background_widget.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0.0113636, x2:1, y2:1, stop:0 rgba(9, 28, 83, 255), stop:1 rgba(138, 41, 115, 255))")
        self.background_widget.setObjectName("background_widget")
        
        vbox_main = QVBoxLayout(self.background_widget)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)

        # Heading
        self.admin_label = QtWidgets.QLabel("Upload .csv File", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(36)
        self.admin_label.setFont(font)
        self.admin_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.admin_label.setAlignment(QtCore.Qt.AlignCenter)
        vbox_main.addWidget(self.admin_label)

        spacer_item = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)


        #Upload Button
        self.uploadButton = QtWidgets.QPushButton("Upload", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        self.uploadButton.setFont(font)
        self.uploadButton.setStyleSheet("""
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
        
        vbox_main.addWidget(self.uploadButton)
        self.uploadButton.clicked.connect(self.upload_csv)


        #CSV Text Edit
        self.csv_preview = QTextEdit(".csv file not yet uploaded", self.background_widget)
        self.csv_preview.setReadOnly(True)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        self.csv_preview.setFont(font)
        self.csv_preview.setStyleSheet("border: 2px solid #FFFFFF;"
                                     "background-color: rgba(0, 0, 0, 0);")
        
        vbox_main.addWidget(self.csv_preview)

        size_policy = self.csv_preview.sizePolicy()
        size_policy.setVerticalPolicy(QSizePolicy.Expanding)
        size_policy.setVerticalStretch(1)
        self.csv_preview.setSizePolicy(size_policy)



        #Submit Button
        self.submitButton = QtWidgets.QPushButton("Submit", self.background_widget)
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

        vbox_main.addWidget(self.submitButton)
        self.submitButton.clicked.connect(self.submit_csv)

        #Question Generation Button
        self.quesGen_button = QtWidgets.QPushButton("Generate Questions", self.background_widget)
        self.quesGen_button.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        self.quesGen_button.setFont(font)
        self.quesGen_button.setStyleSheet("""
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
        
        vbox_main.addWidget(self.quesGen_button)
        self.quesGen_button.clicked.connect(self.quesGen)


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

        button_width = 200  # define the desired width of the buttons
        button_width_back = 105

        # Upload Button
        hbox_uploadButton = QHBoxLayout()
        hbox_uploadButton.addStretch(1)
        self.uploadButton.setFixedWidth(button_width)
        hbox_uploadButton.addWidget(self.uploadButton)
        hbox_uploadButton.addStretch(1)
        vbox_main.addLayout(hbox_uploadButton)


        # Submit Button
        hbox_submitButton = QHBoxLayout()
        hbox_submitButton.addStretch(1)
        self.submitButton.setFixedWidth(button_width)
        hbox_submitButton.addWidget(self.submitButton)
        hbox_submitButton.addStretch(1)
        vbox_main.addLayout(hbox_submitButton)

        # QuesGen Button
        hbox_quesGen_button = QHBoxLayout()
        hbox_quesGen_button.addStretch(1)
        self.quesGen_button.setFixedWidth(button_width)
        hbox_quesGen_button.addWidget(self.quesGen_button)
        hbox_quesGen_button.addStretch(1)
        vbox_main.addLayout(hbox_quesGen_button)

        spacer_item = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)

        # Logout Button
        hbox_backButton = QHBoxLayout()
        hbox_backButton.addStretch(1)
        self.backButton.setFixedWidth(button_width_back)
        hbox_backButton.addWidget(self.backButton)
        hbox_backButton.addStretch(1)
        vbox_main.addLayout(hbox_backButton)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def quesGen(self):
        
        ques = QGen()
        ques.quesGen()
        
        msg = QMessageBox()
        msg.setWindowTitle("Questions successfully generated!")
        msg.setText("Questions successfully generated!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        self.quesGen_button.setEnabled(False)


    def back(self):
        self.backPressed.emit()
        self.close()


    def upload_csv(self):
        # self.submitButton.setEnabled(False)
        # self.quesGen_button.setEnabled(False)
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Upload CSV File", "", "CSV Files (*.csv)", options=options)

        self.shared_data["fileName"] = self.fileName  # Store the uploaded file name
        if self.fileName and not self.fileName == '':
            with open(self.fileName, 'r') as file:
                csv_content = file.read()
                self.csv_preview.setText(csv_content)
            self.submitButton.setEnabled(True)
            self.quesGen_button.setEnabled(True)
    
    def submit_csv(self):
    
        if self.fileName == '':
            # self.quesGen_button.setEnabled(False)
            # # self.submitButton.setEnabled(False)
            msg = QMessageBox()
            msg.setWindowTitle("CSV File Submitted")
            msg.setText("No file selected")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            
        else: 
            ctb = csv_to_DB(self.fileName)
            ctb.insert_CSV()
            self.csv_preview.clear()
            self.fileName = ''
            self.submitButton.setEnabled(False)
            self.quesGen_button.setEnabled(True)