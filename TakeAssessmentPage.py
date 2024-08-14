from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QSpacerItem, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QPushButton
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from mysql.connector import MySQLConnection
import mysql.connector
from GetQuestions import GetQuestions
from PracticeGradesPage import PracticeGradesPage

class TakeAssessmentPage(QtWidgets.QMainWindow):
    backPressed = pyqtSignal()
    backToSPPressed = pyqtSignal()
    
    def __init__(self, assessment_code, student_number):
        super().__init__()

        self.code = assessment_code
        self.stuNo = student_number
        self.l1 = 0
        self.l2 = 0
        self.l3 = 0
        
        self.answer_input = None
        self.vbox_main = None
        self.user_answers = None
        self.current_question_index = 0
        self.user_answer = ""

        self.grades_summary = []
        self.correct_count = 0
        self.all_questions = []
        self.pracGP = None
        
        self.config = {
                "host": "localhost",    
                "user": "root",
                "password": "new_password",
                "database": "admin"
            }

        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor()
        
        self.setUpUi(self)
        self.takeAssessment()
        self.close()
        
    def setUpUi(self, MainWindow):

        MainWindow.setObjectName("Assessment")
        MainWindow.resize(885, 638)
        MainWindow.setMinimumSize(QtCore.QSize(885, 638))

        self.background_widget = QtWidgets.QWidget()
        self.background_widget.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0.0113636, x2:1, y2:1, stop:0 rgba(9, 28, 83, 255), stop:1 rgba(138, 41, 115, 255))")
        self.background_widget.setObjectName("background_widget")
        
        self.vbox_main = QVBoxLayout(self.background_widget)
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vbox_main.addItem(spacer_item)

        # Heading
        self.admin_label = QtWidgets.QLabel("Assessment", self.background_widget)
        font = QtGui.QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(36)
        self.admin_label.setFont(font)
        self.admin_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.admin_label.setAlignment(QtCore.Qt.AlignCenter)
        self.vbox_main.addWidget(self.admin_label)

        spacer_item = QSpacerItem(10, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vbox_main.addItem(spacer_item)

        # Question label
        self.create_label('question_label', "Question")
        self.question_label.setWordWrap(True)
        self.vbox_main.addWidget(self.question_label)
        
        # Answer input
        self.create_line_edit('answer_input')
        self.answer_input.setPlaceholderText("Enter your answer here")
        self.vbox_main.addWidget(self.answer_input)

        spacer_item = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vbox_main.addItem(spacer_item)

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
        
        self.vbox_main.addWidget(self.nextButton)
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
                                        """)
        
        self.vbox_main.addWidget(self.previousQuestion)
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
        
        self.vbox_main.addWidget(self.submitButton)
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
        
        self.vbox_main.addWidget(self.backButton)
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
        self.vbox_main.addLayout(hbox_nextButton)

        # Previous button
        hbox_previousQuestion = QHBoxLayout()
        hbox_previousQuestion.addStretch(1)
        self.previousQuestion.setFixedWidth(button_width)
        hbox_previousQuestion.addWidget(self.previousQuestion)
        hbox_previousQuestion.addStretch(1)
        self.vbox_main.addLayout(hbox_previousQuestion)

        # Submit button
        hbox_submitButton = QHBoxLayout()
        hbox_submitButton.addStretch(1)
        self.submitButton.setFixedWidth(button_width)
        hbox_submitButton.addWidget(self.submitButton)
        hbox_submitButton.addStretch(1)
        self.vbox_main.addLayout(hbox_submitButton)

        # Back button
        hbox_backButton = QHBoxLayout()
        hbox_backButton.addStretch(1)
        self.backButton.setFixedWidth(button_width_back)
        hbox_backButton.addWidget(self.backButton)
        hbox_backButton.addStretch(1)
        self.vbox_main.addLayout(hbox_backButton)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def takeAssessment(self):

        self.user_answers = [] 

        query = "SELECT level1, level2, level3 FROM assessments WHERE assessment_code = %s"
        

        # Database connection details
        config = {
            "host": "localhost",
            "user": "root",
            "password": "new_password",
            "database": "admin"
        }

        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        cursor.execute(query, (self.code,))
        result = cursor.fetchall()

        if result:
            self.l1 = int(result[0][0])
            self.l2 = int(result[0][1])
            self.l3 = int(result[0][2])
            print("Level 1 Questions:", self.l1)
            print("Level 2 Questions:", self.l2)
            print("Level 3 Questions:", self.l3)
        else:
            print("No results found for the given assessment code.")
        
        gq = GetQuestions()
        
        if self.l1 == 0:
            questions_level_one = []
        else:
            questions_level_one = gq.get_questions_from_db(1, self.l1)
            
        if self.l2 == 0:
            questions_level_two = []
        else:
            questions_level_two = gq.get_questions_from_db(2, self.l2)
            
        if self.l3 == 0:
            questions_level_three = []
        else:
            questions_level_three = gq.get_questions_from_db(3, self.l3) 

        self.all_questions = questions_level_one + questions_level_two + questions_level_three

        self.user_answers = [""] * len(self.all_questions)
        self.user_input = [""] * len(self.all_questions)
        
        self.display_question()
        
    def display_question(self):
        if self.current_question_index < len(self.all_questions):
            question_text = self.all_questions[self.current_question_index][0]
            self.question_label.setText(f"Question {self.current_question_index+1}: {question_text}")
            
            if self.current_question_index == 0:
                self.previousQuestion.setDisabled(True)
            else: 
                self.previousQuestion.setDisabled(False)

                if self.current_question_index == len(self.all_questions) - 1:
                    self.nextButton.setDisabled(True)
                    self.submitButton.setDisabled(False)
                else:
                    self.nextButton.setDisabled(False)
                    self.submitButton.setDisabled(True)
        
        else:
            print("Assesment Complete!")
    
    def next_question(self):
            self.user_answer = self.answer_input.text()  # Retrieve the user's answer
            self.user_answers[self.current_question_index] = self.user_answer  # Store the user's input
            self.current_question_index += 1
            self.answer_input.setText(self.user_answers[self.current_question_index])  # Set input box text to stored input
            self.display_question()

    def previous_question(self):
            self.user_answer = self.answer_input.text()  # Retrieve the user's answer
            self.user_answers[self.current_question_index] = self.answer_input.text()
            self.current_question_index -= 1
            self.answer_input.setText(self.user_answers[self.current_question_index]) 
            self.user_answers[self.current_question_index] = self.answer_input.text() 
            self.display_question()

    def submit_assessment(self):  # Adding the missing method
        
        self.close()
        
        user_answer = self.answer_input.text()  # Retrieve the user's answer from the input fieldd
        self.user_answers.insert(self.current_question_index, user_answer)  # Store the user's answer

        config = {
                    "host": "localhost",
                    "user": "root",
                    "password": "new_password",
                    "database": "testSqlDB"
                }

        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()


        for i in range(min(len(self.all_questions), len(self.user_answers))):  # Loop through the user's answers
            user_answer= self.user_answers[i]
            correct_answer = self.all_questions[i][1] # Get the correct answer from the all_questions list
            correct_cursor = connection.cursor()
            correct_cursor.execute(correct_answer)
            correct_result = correct_cursor.fetchall()

            try:
                cursor.execute(user_answer)  # Execute the user's answer
                user_result = cursor.fetchall()

                if correct_result == user_result:
                    print(f"Question {i+1} is correct!")
                    
                    self.correct_count += 1
                else:
                    print(f"Question {i+1} is incorrect!")
                    
            except Exception as e:
                print(f"Question {i+1} is incorrect! Error in execution: {e}")
                
        self.question_label.hide()
        self.answer_input.hide()
        self.nextButton.hide()
        self.submitButton.hide()
        self.previousQuestion.hide()
        self.close()

        self.grades_summary.append(f"You got {self.correct_count} out of {len(self.all_questions)} correct!")

        self.pracGP = PracticeGradesPage(self.grades_summary)
        self.pracGP.show()
        #pracGP.setUpUi(self)
        
        self.grade_percentage = (self.correct_count / len(self.all_questions)) * 100 
        self.pracGP.backPressed.connect(self.backToSP)
        self.store_result_in_db(self.code, self.stuNo, self.grade_percentage)
            
    def store_result_in_db(self, assessment_id, student_number, grade):
            
            cursor = self.connection.cursor()
            query = "INSERT INTO results (userID, assessment_code, grade) VALUES (%s, %s, %s)"
            cursor.execute(query, (student_number, assessment_id, grade))
            self.connection.commit()
            cursor.close()
            
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
        
    def backToSP(self):
        self.backToSPPressed.emit()
        
