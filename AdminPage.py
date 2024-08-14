from PyQt5.QtWidgets import QApplication, QSpacerItem, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from UploadCSVPage import UploadCSVPage
from EditCSVPage import EditCSVPage
from SetAssessmentPage import SetAssessmentPage
from GradesPage import GradesPage


class AdminPage(QtWidgets.QMainWindow):
    backPressed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.upload_csv_page = UploadCSVPage()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Admin")
        MainWindow.resize(885, 638)
        MainWindow.setMinimumSize(QtCore.QSize(885, 638))
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Set up background_widget with linear gradient
        self.background_widget = QtWidgets.QWidget()
        self.background_widget.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(47, 71, 89, 255), stop:1 rgba(10, 23, 59, 255));")
        self.background_widget.setObjectName("background_widget")

        vbox_main = QVBoxLayout(self.background_widget)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)

        #Heading
        self.admin_label = QtWidgets.QLabel("Welcome<br>Administration", self.background_widget)
        self.admin_label.setStyleSheet("""
                background-color: rgba(113, 120, 143, 150);
                font: 26pt "Aptos";
                colour: #1d1d1d;
                margin: 0px;
                padding: 5px;
        """)
        font = QtGui.QFont()
        self.admin_label.setAlignment(QtCore.Qt.AlignLeft)
        self.admin_label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
       
        
        # Create a new layout to contain the label, and align the layout to the left
        label_layout = QtWidgets.QVBoxLayout()
        label_layout.addWidget(self.admin_label, alignment=QtCore.Qt.AlignLeft)
        label_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins around the layout
        vbox_main.addLayout(label_layout)

        # Box for buttons
        box = QtWidgets.QWidget(self.centralwidget)
        box.setStyleSheet("background-color: rgba(113, 120, 143, 150); border-radius: 10px; padding: 20px;")
        button_layout = QtWidgets.QVBoxLayout(box)
        
        #Upload CSV Button
        self.uploadCSV_pushButton = QtWidgets.QPushButton("Upload .csv File", self.background_widget)
        font.setPointSize(17)
        self.uploadCSV_pushButton.setFont(font)
        self.uploadCSV_pushButton.setStyleSheet("""
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


        button_layout.addWidget(self.uploadCSV_pushButton, alignment=QtCore.Qt.AlignLeft)
        self.uploadCSV_pushButton.clicked.connect(self.open_csv_page)

        #Edit CSV Button
        self.editCSV_pushButton = QtWidgets.QPushButton("Edit .csv File", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        self.editCSV_pushButton.setFont(font)
        self.editCSV_pushButton.setStyleSheet("""
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

        
        button_layout.addWidget(self.editCSV_pushButton, alignment=QtCore.Qt.AlignLeft)
        #vbox_main.addWidget(self.editCSV_pushButton)
        self.editCSV_pushButton.clicked.connect(self.open_editcsv_page)  # Connect edit_csv method to the button click signal.


        #View Grades Button
        self.viewGrades_pushButton = QtWidgets.QPushButton("View Grades", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        self.viewGrades_pushButton.setFont(font)
        self.viewGrades_pushButton.setStyleSheet("""
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
        
        #vbox_main.addWidget(self.viewGrades_pushButton)
        button_layout.addWidget(self.viewGrades_pushButton, alignment=QtCore.Qt.AlignLeft)
        self.viewGrades_pushButton.clicked.connect(self.open_grades_page)

        #Set Assessment Button
        self.setAss_pushButton = QtWidgets.QPushButton("Set Assessment", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        self.setAss_pushButton.setFont(font)
        self.setAss_pushButton.setStyleSheet("""
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
        
        #vbox_main.addWidget(self.setAss_pushButton)
        button_layout.addWidget(self.setAss_pushButton, alignment=QtCore.Qt.AlignLeft)
        self.setAss_pushButton.clicked.connect(self.open_assesment_page)

        #vbox_main.addWidget(self.editCSV_pushButton)
        #self.editCSV_pushButton.clicked.connect(self.editCSV)

        #View Queries Button
        self.viewQueries_pushButton = QtWidgets.QPushButton("View Queries", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        self.viewQueries_pushButton.setFont(font)
        self.viewQueries_pushButton.setStyleSheet("""
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
                                                        
        #vbox_main.addWidget(self.viewQueries_pushButton)
        button_layout.addWidget(self.viewQueries_pushButton, alignment=QtCore.Qt.AlignLeft)
        #self.viewQueries_pushButton.clicked.connect(self.viewQueries)

        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)
        
        button_container = QtWidgets.QWidget()
        button_container.setLayout(button_layout)

        vbox_main.addWidget(button_container)


        #Logout Button
        self.logout_pushButton = QtWidgets.QPushButton("Logout", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(15)
        self.logout_pushButton.setFont(font)
        self.logout_pushButton.setStyleSheet("""
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

        
        vbox_main.addWidget(self.logout_pushButton)
        self.logout_pushButton.clicked.connect(self.back)

        
    
        MainWindow.setCentralWidget(self.background_widget)  # Set background_widget as the central widget

        button_width = 200  # define the desired width of the buttons
        button_width_back = 105

        # Set Assessment Button
        hbox_setAss = QHBoxLayout()
        hbox_setAss.addStretch(1)
        self.setAss_pushButton.setFixedWidth(button_width)
        hbox_setAss.addWidget(self.setAss_pushButton)
        hbox_setAss.addStretch(1)
        vbox_main.addLayout(hbox_setAss)
        
        # Upload .csv Button
        hbox_uploadCSV = QHBoxLayout()
        hbox_uploadCSV.addStretch(1)
        self.uploadCSV_pushButton.setFixedWidth(button_width)
        hbox_uploadCSV.addWidget(self.uploadCSV_pushButton)
        hbox_uploadCSV.addStretch(1)
        vbox_main.addLayout(hbox_uploadCSV)
        
        # Edit CSV Button
        hbox_editCSV = QHBoxLayout()
        hbox_editCSV.addStretch(1)
        self.editCSV_pushButton.setFixedWidth(button_width)
        hbox_editCSV.addWidget(self.editCSV_pushButton)
        hbox_editCSV.addStretch(1)
        vbox_main.addLayout(hbox_editCSV)
        
        # View Grades Button
        hbox_viewGrades = QHBoxLayout()
        hbox_viewGrades.addStretch(1)
        self.viewGrades_pushButton.setFixedWidth(button_width)
        hbox_viewGrades.addWidget(self.viewGrades_pushButton)
        hbox_viewGrades.addStretch(1)
        vbox_main.addLayout(hbox_viewGrades)
        
        # View Queries Button
        hbox_viewQueries = QHBoxLayout()
        hbox_viewQueries.addStretch(1)
        self.viewQueries_pushButton.setFixedWidth(button_width)
        hbox_viewQueries.addWidget(self.viewQueries_pushButton)
        hbox_viewQueries.addStretch(1)
        vbox_main.addLayout(hbox_viewQueries)

        spacer_item = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)

        # Logout Button
        hbox_logout = QHBoxLayout()
        hbox_logout.addStretch(1)
        self.logout_pushButton.setFixedWidth(button_width_back)
        hbox_logout.addWidget(self.logout_pushButton)
        hbox_logout.addStretch(1)
        vbox_main.addLayout(hbox_logout)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.admin_label.setText(_translate("MainWindow", "Administration"))
        self.uploadCSV_pushButton.setText(_translate("MainWindow", "Upload .csv File"))
        self.logout_pushButton.setText(_translate("MainWindow", "logout"))
        self.viewGrades_pushButton.setText(_translate("MainWindow", "View Grades"))
        self.setAss_pushButton.setText(_translate("MainWindow", "Set Assessment"))
        self.editCSV_pushButton.setText(_translate("MainWindow", "Edit .csv File"))
        self.viewQueries_pushButton.setText(_translate("MainWindow", "View Queries"))
    
    def show_admin_page(self):
        self.show()
    
    def open_csv_page(self):
        self.csv_page = UploadCSVPage()
        self.csv_page.show()
        self.csv_page.backPressed.connect(self.show_admin_page)
        self.close()

    def open_editcsv_page(self):
        self.editcsv_page = EditCSVPage() 
        self.editcsv_page.show()
        self.editcsv_page.backPressed.connect(self.show_admin_page)
        self.close()

    def open_grades_page(self):
        self.grades_page = GradesPage()
        self.grades_page.show()
        self.grades_page.backPressed.connect(self.show_admin_page)
        self.close()

    def back(self):
        self.backPressed.emit()
        self.close()
    
    def open_assesment_page(self):
        self.set_assesment_page = SetAssessmentPage()
        self.set_assesment_page.show()
        self.set_assesment_page.backPressed.connect(self.show_admin_page)
        self.close()
