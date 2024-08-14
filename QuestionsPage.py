import pandas as pd
import mysql.connector
from PyQt5.QtWidgets import QApplication, QSpacerItem, QVBoxLayout, QHBoxLayout, QSizePolicy, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PracticeGradesPage import PracticeGradesPage

class QuestionsPage(QtWidgets.QMainWindow):
    
    submitted = pyqtSignal()
    backPressed = pyqtSignal()
    
    def __init__(self, questions):
        super().__init__()
        self.questions = questions
        self.user_answers = [""] * len(self.questions)
        self.user_input = [""] * len(self.questions)
        self.user_answer = ""
        self.grades_summary = []
        self.submit = False
        self.current_question_index = 0
        
        
        config = {
            "host": "localhost",
            "user": "root",
            "password": "new_password",
            "database": "testSqlDB"
        }

        self.connection = mysql.connector.connect(**config)
        self.setUpUi(self)

    def setUpUi(self, MainWindow):

        MainWindow.setObjectName("Practice Assessment")
        MainWindow.resize(885, 638)
        MainWindow.setMinimumSize(QtCore.QSize(885, 638))

        self.background_widget = QtWidgets.QWidget()
        self.background_widget.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0.0113636, x2:1, y2:1, stop:0 rgba(9, 28, 83, 255), stop:1 rgba(138, 41, 115, 255))")
        self.background_widget.setObjectName("background_widget")
        
        vbox_main = QVBoxLayout(self.background_widget)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)

        # Heading
        self.admin_label = QtWidgets.QLabel("Practice Assessment", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(36)
        self.admin_label.setFont(font)
        self.admin_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.admin_label.setAlignment(QtCore.Qt.AlignCenter)
        vbox_main.addWidget(self.admin_label)

        spacer_item = QSpacerItem(10, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)

#######
        # Question label
        self.create_label('question_label', "Question")
        self.question_label.setWordWrap(True)
        vbox_main.addWidget(self.question_label)
        
        # Answer input
        self.create_line_edit('answer_input')
        self.answer_input.setPlaceholderText("Enter your answer here")
        vbox_main.addWidget(self.answer_input)

        spacer_item = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vbox_main.addItem(spacer_item)

        # Next button
        self.nextButton = QtWidgets.QPushButton("Next Question", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        self.nextButton.setFont(font)
        self.nextButton.setStyleSheet("""
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
        
        vbox_main.addWidget(self.nextButton)
        self.nextButton.clicked.connect(self.next_question)
    
        # Previous button
        self.previousQuestion = QtWidgets.QPushButton("Previous Question", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        self.previousQuestion.setFont(font)
        self.previousQuestion.setStyleSheet("""
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
        
        vbox_main.addWidget(self.previousQuestion)
        self.previousQuestion.clicked.connect(self.previous_question)

        # Submit button
        self.submitButton = QtWidgets.QPushButton("Submit Assessment", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
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
                                       
                                QPushButton:pressed{
                                    background-color: rgb(37, 148, 70);
                                }
                                """)
        
        vbox_main.addWidget(self.submitButton)
        self.submitButton.clicked.connect(self.submit_assessment)


        # Back button
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

        button_width = 200  # define the desired width of the buttons
        button_width_back = 105


        # Next button
        hbox_nextButton = QHBoxLayout()
        hbox_nextButton.addStretch(1)
        self.nextButton.setFixedWidth(button_width)
        hbox_nextButton.addWidget(self.nextButton)
        hbox_nextButton.addStretch(1)
        vbox_main.addLayout(hbox_nextButton)

        # Previous button
        hbox_previousQuestion = QHBoxLayout()
        hbox_previousQuestion.addStretch(1)
        self.previousQuestion.setFixedWidth(button_width)
        hbox_previousQuestion.addWidget(self.previousQuestion)
        hbox_previousQuestion.addStretch(1)
        vbox_main.addLayout(hbox_previousQuestion)

        # Submit button
        hbox_submitButton = QHBoxLayout()
        hbox_submitButton.addStretch(1)
        self.submitButton.setFixedWidth(button_width)
        hbox_submitButton.addWidget(self.submitButton)
        hbox_submitButton.addStretch(1)
        vbox_main.addLayout(hbox_submitButton)

        # Back button
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


        # Initialize question index and display the first question

        self.display_question()

    def back(self):
        self.backPressed.emit()
        self.close()
    
    def display_question(self):
        if self.current_question_index < len(self.questions):
            question_text = self.questions[self.current_question_index][0]
            self.question_label.setText(f"Question {self.current_question_index+1}:\n{question_text}")
            
        if self.current_question_index == 0:
            self.previousQuestion.setDisabled(True)
        else: 
            self.previousQuestion.setDisabled(False)

        # Check if this is the last question and disable the Next button if it is
        if self.current_question_index == len(self.questions) - 1:
            self.nextButton.setDisabled(True)
            self.submitButton.setDisabled(False)

        else:
            self.nextButton.setDisabled(False)
            self.submitButton.setDisabled(True)

            print(self.user_answers)
            print(self.current_question_index)

    def next_question(self):
        self.user_answer = self.answer_input.text()  # Retrieve the user's answer
        self.user_answers[self.current_question_index] = self.user_answer  # Store the user's input
        self.current_question_index += 1
        self.display_question()
        self.answer_input.setText(self.user_answers[self.current_question_index])  # Set input box text to stored input
        #self.display_question()

    def previous_question(self):
        self.user_answer = self.answer_input.text()  # Retrieve the user's answer
        self.user_answers[self.current_question_index] = self.answer_input.text()
        self.current_question_index -= 1
        self.answer_input.setText(self.user_answers[self.current_question_index]) 
        self.user_answers[self.current_question_index] = self.answer_input.text() 
        self.display_question()

    def submit_assessment(self):  # Adding the missing method
        # user_answer = self.answer_input.text()  # Retrieve the user's answer from the input fieldd
        # self.user_answers.insert(self.current_question_index, user_answer)  # Store the user's answer
        self.user_answer = self.answer_input.text()  # Retrieve the user's answer
        self.user_answers[self.current_question_index] = self.answer_input.text()
        print(self.user_answers)
       # print("final index" + self.current_question_index)
        cursor = self.connection.cursor()
        correct_count = 0
        self.grades_summary = []
        for i in range(min(len(self.questions), len(self.user_answers))):  # Loop through the user's answers
                user_answer= self.user_answers[i]
                correct_answer = self.questions[i][1] # Get the correct answer from the all_questions list
                correct_cursor = self.connection.cursor()
                correct_cursor.execute(correct_answer)
                correct_result = correct_cursor.fetchall()

                try:
                    cursor.execute(user_answer)
                    user_result = cursor.fetchall()

                    if correct_result == user_result:
                        print(f"Question {i+1} is correct!")
                        self.grades_summary.append(f"Question {i+1} is correct!")
                        correct_count += 1
                    else:
                        print(f"Question {i+1} is incorrect!")
                        self.grades_summary.append(f"Question {i+1} is incorrect!")
                except Exception as e:
                    print(f"Question {i+1} is incorrect! Error in execution: {e}")
                    self.grades_summary.append(f"Question {i+1} is incorrect! Error in execution: {e}")

        print(f"You got {correct_count} out of {len(self.questions)} correct!")
        self.submitted.emit()
        
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
        