from PyQt5.QtWidgets import QApplication, QSizePolicy, QSpacerItem, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from GetGrades import GetGrades

class GradesPage(QtWidgets.QMainWindow):
    backPressed = pyqtSignal()
    

    def __init__(self):
        super().__init__()
        self.setupUi(self)
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Grades")
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
        self.admin_label = QtWidgets.QLabel("View Grades", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(36)
        self.admin_label.setFont(font)
        self.admin_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.admin_label.setAlignment(QtCore.Qt.AlignCenter)
        vbox_main.addWidget(self.admin_label)

        spacer_item = QSpacerItem(10, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)

        #Assessment ID label
        self.create_label('assess_id_label', "Enter Assessment ID")
        vbox_main.addWidget(self.assess_id_label, 0, QtCore.Qt.AlignCenter)

        #Assessment ID Line Edit
        self.create_line_edit('assess_id_input')
        vbox_main.addWidget(self.assess_id_input, 0, QtCore.Qt.AlignCenter)
        self.assess_id_input.returnPressed.connect(self.enter)

        spacer_item = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)

        # Create and configure the QTableWidget
        self.tableWidget = QtWidgets.QTableWidget(self.background_widget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)  # Set the number of columns as needed

        # Set the table headers
        self.tableWidget.setHorizontalHeaderLabels(['AssessmentID', 'StudentNumber', 'Grade'])
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

        #Enter Button
        self.enterButton = QtWidgets.QPushButton("Enter", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        self.enterButton.setFont(font)
        self.enterButton.setStyleSheet("""
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
                                       
                                QPushButton:pressed{
                                    background-color: rgb(37, 148, 70);
                                }
                                """)
        
        vbox_main.addWidget(self.enterButton)
        self.enterButton.clicked.connect(self.enter)

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

        #Enter Button
        hbox_enterButton = QHBoxLayout()
        hbox_enterButton.addStretch(1)
        self.enterButton.setFixedWidth(button_width)
        hbox_enterButton.addWidget(self.enterButton)
        hbox_enterButton.addStretch(1)
        vbox_main.addLayout(hbox_enterButton)

        # Back Button
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

    def enter(self):
        assessment_id = self.assess_id_input.text()
        self.gg = GetGrades(assessment_id)
        
        if not assessment_id:
            msg = QMessageBox()
            msg.setWindowTitle("Input Error")
            msg.setText("Please enter an assessment code.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            
        else: 
                # Check if the assessment code exists
            if self.gg.assessment_exists(assessment_id):
                # Check if there are no results for the assessment code
                if not self.gg.results_exist(assessment_id):
                    msg = QMessageBox()
                    msg.setWindowTitle("No Results")
                    msg.setText("No results for this assessment")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()
                else:
                    # Display results
                    self.display_grades(self.gg.get_grades())
            else:
                # Display an error message if the assessment code does not exist
                msg = QMessageBox()
                msg.setWindowTitle("Assessment Not Found")
                msg.setText("Assessment code not found.")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
  
    def display_grades(self, grades):
        self.tableWidget.setRowCount(len(grades))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Student Number', 'Assessment Code', 'Grade'])
        
        for row, grade in enumerate(grades):
            for column, item in enumerate(grade):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))