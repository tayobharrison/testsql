from PyQt5.QtWidgets import QApplication, QSizePolicy, QSpacerItem, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from TakeAssessmentPage import TakeAssessmentPage
from GetGrades import GetGrades

class AssessmentPage(QtWidgets.QMainWindow):
    backPressed = pyqtSignal()

    def __init__(self, studentNum):
        super().__init__()
        self.setupUi(self, studentNum)

    def setupUi(self, MainWindow, studentNum):
        MainWindow.setObjectName("Begin Assessment")
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
        self.admin_label = QtWidgets.QLabel("Begin Assessment", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(36)
        self.admin_label.setFont(font)
        self.admin_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.admin_label.setAlignment(QtCore.Qt.AlignCenter)
        vbox_main.addWidget(self.admin_label)

        spacer_item = QSpacerItem(10, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)

        # Student Number label
        self.create_label('studentNum_label', "Student Number:")
        vbox_main.addWidget(self.studentNum_label, 0, QtCore.Qt.AlignCenter)

       # Student Number input
        self.create_line_edit('stuNum_input')
        vbox_main.addWidget(self.stuNum_input, 0, QtCore.Qt.AlignCenter)

        spacer_bottom = QSpacerItem(5, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_bottom)

        # Assessment code label
        self.create_label('assessCode_label', "Assessment Code:")
        vbox_main.addWidget(self.assessCode_label, 0, QtCore.Qt.AlignCenter)

       # Assessment Code input
        self.create_line_edit('assessCode_input')
        vbox_main.addWidget(self.assessCode_input, 0, QtCore.Qt.AlignCenter)

        spacer_bottom = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_bottom)

        # Begin button
        self.submitButton = QtWidgets.QPushButton("Begin", self.background_widget)
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
        self.submitButton.clicked.connect(self.submit_assessment_code)
        #self.submitButton.returnPressed.connect(self.submit_assessment_code)

        spacer_bottom = QSpacerItem(5, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_bottom)

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
        
        MainWindow.setCentralWidget(self.background_widget) 

        button_width = 200
        button_width_back = 105

        #Back Button
        hbox_backButton = QHBoxLayout()
        hbox_backButton.addStretch(1)
        self.backButton.setFixedWidth(button_width_back)
        hbox_backButton.addWidget(self.backButton)
        hbox_backButton.addStretch(1)
        vbox_main.addLayout(hbox_backButton)

        #Submit Button
        hbox_submitButton = QHBoxLayout()
        hbox_submitButton.addStretch(1)
        self.submitButton.setFixedWidth(button_width)
        hbox_submitButton.addWidget(self.submitButton)
        hbox_submitButton.addStretch(1)
        vbox_main.addLayout(hbox_submitButton)

        self.stuNum = studentNum

    def back(self):
        self.backPressed.emit()
        self.close()

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


    def submit_assessment_code(self):
        code = self.assessCode_input.text()
        student_number = self.stuNum_input.text().lower()
        print(student_number)
        print(self.stuNum)
        
        gg = GetGrades()

        if gg.assessment_exists(code) and not (student_number == self.stuNum):
            msg = QMessageBox()
            msg.setWindowTitle("Input Error")
            msg.setText("Please enter your student number.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        elif (student_number == self.stuNum) and not gg.assessment_exists(code):
            msg = QMessageBox()
            msg.setWindowTitle("Input Error")
            msg.setText("Please enter a valid assessment code.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        elif not (gg.assessment_exists(code) and student_number == self.stuNum):
            msg = QMessageBox()
            msg.setWindowTitle("Input Error")
            msg.setText("Please enter your student number and a valid assessment code.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        elif gg.alreadyTaken(student_number, code):
            msg = QMessageBox()
            msg.setWindowTitle("Input Error")
            msg.setText("You have already taken this assessment.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        else:
            self.take_assessment_page = TakeAssessmentPage(code, student_number)
            self.take_assessment_page.show()
            self.take_assessment_page.backPressed.connect(self.back)
            self.take_assessment_page.backToSPPressed.connect(self.back)
            self.close()