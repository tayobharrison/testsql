from PyQt5.QtWidgets import QApplication, QSpacerItem, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QSizePolicy, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from AssessmentPage import AssessmentPage
from PracticePage import PracticePage


class StudentPage(QtWidgets.QMainWindow):
    backPressed = pyqtSignal()
    
    def __init__(self, studentNum):
        super().__init__()
        self.practice_page = None
        self.setupUi(self)
        self.studentNum = studentNum

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(885, 638)
        MainWindow.setMinimumSize(QtCore.QSize(885, 638))

        # Set up background_widget with linear gradient
        self.background_widget = QtWidgets.QWidget()
        self.background_widget.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0.0113636, x2:1, y2:1, stop:0 rgba(9, 28, 83, 255), stop:1 rgba(138, 41, 115, 255))")
        self.background_widget.setObjectName("background_widget")


        vbox_main = QVBoxLayout(self.background_widget)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)
        self.admin_label = QtWidgets.QLabel("Welcome!", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(36)
        self.admin_label.setFont(font)
        self.admin_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.admin_label.setAlignment(QtCore.Qt.AlignCenter)
        vbox_main.addWidget(self.admin_label)


        self.continue_prac_button = QtWidgets.QPushButton('Continue Practice', self.background_widget)
        self.continue_prac_button.setDisabled(True)
        font.setPointSize(17)
        self.continue_prac_button.setFont(font)
        self.continue_prac_button.setStyleSheet("""
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
        vbox_main.addWidget(self.continue_prac_button)

        self.continue_prac_button.clicked.connect(self.open_cont_practice_page)

        self.new_prac_button = QtWidgets.QPushButton("New Practice", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        self.new_prac_button.setFont(font)
        self.new_prac_button.setStyleSheet("""
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
        
        vbox_main.addWidget(self.new_prac_button)
        self.new_prac_button.clicked.connect(self.open_practice_page)

        self.assess_button = QPushButton('Take Assesment', self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        self.assess_button.setFont(font)
        self.assess_button.setStyleSheet("""
                                QPushButton {
                                    background-color: rgb(87, 198, 120);
                                    color: rgb(255, 255, 255);
                                    border-radius: 10px;
                                    padding: 5px;
                                }
                                         
                                QPushButton:hover {
                                    background-color: rgb(57, 168, 90);
                                    color: rgb(255, 255, 255);
                                }
                                
                                QPushButton:pressed {
                                    background-color: rgb(37, 148, 70);
                                }
                                """)

        vbox_main.addWidget(self.assess_button)
        self.assess_button.clicked.connect(self.open_assessment_page)
    
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)

        self.backButton = QtWidgets.QPushButton("Logout", self.background_widget)
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

        #Continue Prac Button
        hbox_continue_prac = QHBoxLayout()
        hbox_continue_prac.addStretch(1)
        self.continue_prac_button.setFixedWidth(button_width)
        hbox_continue_prac.addWidget(self.continue_prac_button)
        hbox_continue_prac.addStretch(1)
        vbox_main.addLayout(hbox_continue_prac)

        #New Prac Button
        hbox_new_prac = QHBoxLayout()
        hbox_new_prac.addStretch(1)
        self.new_prac_button.setFixedWidth(button_width)
        hbox_new_prac.addWidget(self.new_prac_button)
        hbox_new_prac.addStretch(1)
        vbox_main.addLayout(hbox_new_prac)

        #Assess Button
        hbox_assess_prac = QHBoxLayout()
        hbox_assess_prac.addStretch(1)
        self.assess_button.setFixedWidth(button_width)
        hbox_assess_prac.addWidget(self.assess_button)
        hbox_assess_prac.addStretch(1)
        vbox_main.addLayout(hbox_assess_prac)
        
        spacer_item = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)
        
        #Back Button
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
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.admin_label.setText(_translate("MainWindow", "Welcome"))
        self.continue_prac_button.setText(_translate("MainWindow", "Continue Practice"))
        self.new_prac_button.setText(_translate("MainWindow", "New Practice"))
        self.prev_prac_button.setText(_translate("MainWindow", "Previous Practice"))
        self.assess_button.setText(_translate("MainWindow", "Take Assessment"))
        self.back_button.setText(_translate("MainWindow", "Logout"))


    @pyqtSlot()   
    def show_student_page(self):
        self.show()

    def open_practice_page(self):
        self.practice_page = PracticePage()
        self.practice_page.show()
        self.practice_page.started.connect(self.disableButton)
        self.practice_page.backPressed.connect(self.show_student_page)
        self.practice_page.submitted.connect(self.enableButton)
        self.close()
        
    def disableButton(self):
        self.new_prac_button.setDisabled(True)
        self.continue_prac_button.setDisabled(False)
        
        
    def enableButton(self):
        self.new_prac_button.setDisabled(False)
        self.continue_prac_button.setDisabled(True)

    def open_cont_practice_page(self):
        self.practice_page.question_page.show()
        self.close()

    def open_assessment_page(self):
        self.assessment_page = AssessmentPage(self.studentNum)  # Pass the student number as an argument
        self.assessment_page.show()
        self.assessment_page.backPressed.connect(self.show_student_page)
        self.close()

    def back(self):
        self.backPressed.emit()
        self.close()