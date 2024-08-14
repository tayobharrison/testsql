import sys
from PyQt5.QtWidgets import QApplication, QSizePolicy, QSpacerItem, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from GetQuestions import GetQuestions
from PyQt5 import QtCore, QtGui, QtWidgets
from QuestionsPage import QuestionsPage
from PracticeGradesPage import PracticeGradesPage

class PracticePage(QtWidgets.QMainWindow):
    
    backPressed = pyqtSignal()
    submitted = pyqtSignal()
    started = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.question_page = None
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Practice Page")
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
        self.admin_label = QtWidgets.QLabel("Select Number of Questions", self.background_widget)
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

        # Start practice Button
        self.startPrac_button = QtWidgets.QPushButton("Start Practice", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        self.startPrac_button.setFont(font)
        self.startPrac_button.setStyleSheet("""
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
        
        vbox_main.addWidget(self.startPrac_button)
        self.startPrac_button.clicked.connect(self.start_practice)
        self.startPrac_button.setEnabled(False)

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

        
        self.level1_input.textChanged.connect(self.update_start_button_state)
        self.level2_input.textChanged.connect(self.update_start_button_state)
        self.level3_input.textChanged.connect(self.update_start_button_state)
        
        self.startPrac_button.clicked.connect(self.clear_text_fields)

        button_width = 200
        button_width_back = 105

        #Start Button
        hbox_startPrac_button = QHBoxLayout()
        hbox_startPrac_button.addStretch(1)
        self.startPrac_button.setFixedWidth(button_width)
        hbox_startPrac_button.addWidget(self.startPrac_button)
        hbox_startPrac_button.addStretch(1)
        vbox_main.addLayout(hbox_startPrac_button)

        #Back Button
        hbox_backButton = QHBoxLayout()
        hbox_backButton.addStretch(1)
        self.backButton.setFixedWidth(button_width_back)
        hbox_backButton.addWidget(self.backButton)
        hbox_backButton.addStretch(1)
        vbox_main.addLayout(hbox_backButton)



    @pyqtSlot()
    
    def update_start_button_state(self):
        # Enable the button if there is text in all input fields, otherwise disable it
        enable_button = bool(self.level1_input.text() and
                            self.level2_input.text() and
                            self.level3_input.text())
        self.startPrac_button.setEnabled(enable_button)
    
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

    @pyqtSlot()
    def clear_text_fields(self):
        # Clear all text fields when the button is clicked
        self.level1_input.clear()
        self.level2_input.clear()
        self.level3_input.clear()

    def back(self):
        self.backPressed.emit()
        self.close()

    def start_practice(self):
        
        try: 
            number_of_questions_one = int(self.level1_input.text())
            number_of_questions_two = int(self.level2_input.text())
            number_of_questions_three = int(self.level3_input.text())
            
            # Get questions from database
            gq = GetQuestions()
            
            if number_of_questions_one == 0:
                questions_level_one = []
            else:
                questions_level_one = gq.get_questions_from_db(1, number_of_questions_one)
                
            if number_of_questions_two == 0:
                questions_level_two = []
            else:
                questions_level_two = gq.get_questions_from_db(2, number_of_questions_two)
                
            if number_of_questions_three == 0:
                questions_level_three = []
            else:
                questions_level_three = gq.get_questions_from_db(3, number_of_questions_three) 

            self.all_questions = questions_level_one + questions_level_two + questions_level_three

            if len(self.all_questions) == 0:
                msg = QMessageBox()
                msg.setText("You did not specify any number of levels.")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()

            else:    
                self.question_page = QuestionsPage(self.all_questions)
                self.question_page.show()
                self.close()
                self.question_page.submitted.connect(self.show_practice_grades)
                self.question_page.backPressed.connect(self.back)
                #blur out New Practice button- signal
                self.started.emit()

            
        except ValueError:
            # If conversion fails, display error message
            msg = QMessageBox()
            msg.setWindowTitle("Input Error")
            msg.setText("Only numbers can be input for question level.")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        
    @pyqtSlot()
    def show_practice_grades(self):
        #self.question_page.close()  # Close the QuestionsPage
        self.submitted.emit()
        self.practice_grades_page = PracticeGradesPage(self.question_page.grades_summary)
        self.practice_grades_page.show()
        self.practice_grades_page.backPressed.connect(self.back)
        self.question_page.close()