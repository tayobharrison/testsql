from PyQt5.QtWidgets import QApplication, QSpacerItem, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QSizePolicy, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

class PracticeGradesPage(QtWidgets.QMainWindow):
    
    backPressed = pyqtSignal()
    
    def __init__(self, grades_summary):
        super().__init__()

        self.grades_summary = grades_summary
        self.setUpUi(self)


    def setUpUi(self, MainWindow):
        MainWindow.setObjectName("Results")
        MainWindow.resize(885, 638)
        MainWindow.setMinimumSize(QtCore.QSize(885, 638))

        self.background_widget = QtWidgets.QWidget()
        self.background_widget.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0.0113636, x2:1, y2:1, stop:0 rgba(9, 28, 83, 255), stop:1 rgba(138, 41, 115, 255))")
        self.background_widget.setObjectName("background_widget")
        
        vbox_main = QVBoxLayout(self.background_widget)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)

        # Heading
        self.admin_label = QtWidgets.QLabel("Results", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(36)
        self.admin_label.setFont(font)
        self.admin_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.admin_label.setAlignment(QtCore.Qt.AlignCenter)
        vbox_main.addWidget(self.admin_label)

        spacer_item = QSpacerItem(10, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)

        # Grades summary text edit
        self.grades_text = QTextEdit("hello", self.background_widget)
        self.grades_text.setReadOnly(True)
        self.grades_text.setText("\n".join(self.grades_summary))
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        self.grades_text.setFont(font)
        self.grades_text.setStyleSheet("border: 2px solid #FFFFFF;"
                                     "background-color: rgba(0, 0, 0, 0);")
        
        vbox_main.addWidget(self.grades_text)
        
        size_policy = self.grades_text.sizePolicy()
        size_policy.setVerticalPolicy(QSizePolicy.Expanding)
        size_policy.setVerticalStretch(1)
        self.grades_text.setSizePolicy(size_policy)

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
        MainWindow.show()
        button_width_back = 105

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

    def back(self):
        self.backPressed.emit()
        self.close()