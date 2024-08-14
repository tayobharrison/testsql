import sys
from PyQt5.QtWidgets import QApplication, QSizePolicy, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt, pyqtSlot
from checkLogin import checkLogin
from Assessment import Assessment
from GetQuestions import GetQuestions
from GetGrades import GetGrades
from csv_to_DB import csv_to_DB
from QuestionsPage import QuestionsPage
from tkinter import *

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800,600)
        self.setWindowTitle('Login Page')
        layout = QVBoxLayout()

        self.user_id_label = QLabel('User ID')
        layout.addWidget(self.user_id_label)
        self.user_id_input = QLineEdit()
        layout.addWidget(self.user_id_input)


        self.password_label = QLabel('Password')
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        login_button = QPushButton('Login')
        login_button.clicked.connect(self.check_login)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def check_login(self):
        user_id = self.user_id_input.text()
        password = self.password_input.text()

        cl = checkLogin()

        # Here you can check the user_id and password against the database
        # If the user_id and password are correct, you can open the student or admin page based on role
        user_role = cl.verify(user_id, password)

        if user_role == 0:
            self.open_student_page()
        elif user_role == 1:
            self.open_admin_page()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Login Failed")
            msg.setText("Invalid User ID or Password!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    #show student page
    def open_student_page(self):
        self.student_page = StudentPage()
        self.student_page.show()
        self.close()

    #show admin page
    def open_admin_page(self):
        self.admin_page = AdminPage()
        self.admin_page.show()
        self.close()
        
class StudentPage(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800,600)
        self.setWindowTitle('Student Page')

        layout = QVBoxLayout()

        button1 = QPushButton('Practice')
        button1.clicked.connect(self.open_practice_page)
        layout.addWidget(button1)

        button2 = QPushButton('Assesment')
        button2.clicked.connect(self.open_assesment_page)
        layout.addWidget(button2)

        backButton = QPushButton('Back')
        backButton.clicked.connect(self.back)
        layout.addWidget(backButton)

        self.setLayout(layout)

    def open_practice_page(self):
        self.practice_page = PracticePage()
        self.practice_page.show()
        self.close()

    def open_assesment_page(self):
        self.assesment_page = AssesmentPage()
        self.assesment_page.show()
        self.close()

    def back(self):
        self.login_page = LoginPage()
        self.login_page.show()
        self.close()

class AdminPage(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800,600)
        self.setWindowTitle('Admin Page')

        layout = QVBoxLayout()

        button1 = QPushButton('Upload CSV')
        button1.clicked.connect(self.open_csv_page)
        layout.addWidget(button1)

        button2 = QPushButton('View Grades')
        button2.clicked.connect(self.open_grades_page)
        layout.addWidget(button2)

        button_setAssesment = QPushButton('Set Assesment')
        button_setAssesment.clicked.connect(self.open_assesment_page)
        layout.addWidget(button_setAssesment)

        backButton = QPushButton('Back')
        backButton.clicked.connect(self.back)
        layout.addWidget(backButton)

        self.setLayout(layout)
    
    def open_csv_page(self):
        self.csv_page = CSVPage()
        self.csv_page.show()
        self.close()

    def open_grades_page(self):
        self.grades_page = GradesPage()
        self.grades_page.show()
        self.close()

    def back(self):
        self.login_page = LoginPage()
        self.login_page.show()
        self.close()
    
    def open_assesment_page(self):
        self.set_assesment_page = SetAssessmentPage()
        self.set_assesment_page.show()
        self.close()

class SetAssessmentPage(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle('Set Assessment Page')

        layout = QVBoxLayout()

        # Fields to enter the number of questions for each level
        self.level1_input = QLineEdit()
        self.level1_input.setPlaceholderText('Number of Level 1 Questions:')
        layout.addWidget(self.level1_input)

        self.level2_input = QLineEdit()
        self.level2_input.setPlaceholderText('Number of Level 2 Questions:')
        layout.addWidget(self.level2_input)

        self.level3_input = QLineEdit()
        self.level3_input.setPlaceholderText('Number of Level 3 Questions:')
        layout.addWidget(self.level3_input)

        # Field to enter the assessment code
        code_label = QLabel('Assessment Code:')
        layout.addWidget(code_label)
        self.code_input = QLineEdit()
        layout.addWidget(self.code_input)

        # Button to generate the assessment
        create_button = QPushButton('Create Assessment')
        create_button.clicked.connect(self.create_assessment)
        layout.addWidget(create_button)

        # Button to go back
        back_button = QPushButton('Back')
        back_button.clicked.connect(self.back)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def create_assessment(self):
        # Retrieve the number of questions for each level, and the assessment code
        level1_questions = int(self.level1_input.text())
        level2_questions = int(self.level2_input.text())
        level3_questions = int(self.level3_input.text())
        assessment_code = self.code_input.text()

        assess = Assessment()
        assess.createAssessment(level1_questions, level2_questions, level3_questions, assessment_code)

    def back(self):
        self.admin_page = AdminPage()
        self.admin_page.show()
        self.close()

class AssesmentPage(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle('Assessment Page')

        layout = QVBoxLayout()  # Define layout first

        # Label and input for student number
        studentNum_label = QLabel('Enter Student Number')
        studentNum_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(studentNum_label)
        self.studentNum_input = QLineEdit()
        layout.addWidget(self.studentNum_input)

        # Label and input for assessment code
        code_label = QLabel('Enter Assessment Code')
        code_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(code_label)
        self.code_input = QLineEdit()
        layout.addWidget(self.code_input)

        # Submit and back buttons
        submitButton = QPushButton('Begin Assessment')
        submitButton.clicked.connect(self.submit_assessment_code)
        layout.addWidget(submitButton)

        backButton = QPushButton('Back')
        backButton.clicked.connect(self.back)
        layout.addWidget(backButton)

        self.setLayout(layout)  # Set layout

    def back(self):
        self.student_page = StudentPage()
        self.student_page.show()
        self.close()

    def submit_assessment_code(self):
        code = self.code_input.text()
        student_number = self.studentNum_input.text()
        print("Entered Assessment Code:", code)
        print("Entered Student Number:", student_number)

        self.take_assessment_page = takeAssesmentPage(code, student_number)
        self.take_assessment_page.show()
        
        self.close()

class takeAssesmentPage(QWidget):
    def __init__(self, assessment_code, student_number):
        super().__init__()
        self.resize(800,600)
        self.setWindowTitle("Take Assesment Page")
        self.assessment_code = assessment_code
        self.student_number = student_number
        self.level1_questions = 0
        self.level2_questions = 0
        self.level3_questions = 0

        backButton = QPushButton('Back')
        backButton.clicked.connect(self.back)
        
        self.assess = Assessment()
        self.assess.takeAssessment(self.assessment_code, self.student_number, self.level1_questions, self.level2_questions, self.level3_questions)
        # self.practice_grades_page = PracticeGradesPage(self.ta.grades_summary)
        # self.practice_grades_page.show()
        self.close()
        self.assess.layout.addWidget(backButton)
        self.setLayout(self.assess.layout)
    
    def back(self):
        self.student_page = StudentPage()
        self.student_page.show()
        self.close()
        
class PracticePage(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800,600)
        self.setWindowTitle('Practice Page')

        layout = QVBoxLayout()

        # Level ONE
        level_one_label = QLabel('Level ONE (Enter number of questions):')
        layout.addWidget(level_one_label)
        self.level_one_input = QLineEdit()
        layout.addWidget(self.level_one_input)

        # Level TWO
        level_two_label = QLabel('Level TWO (Enter number of questions):')
        layout.addWidget(level_two_label)
        self.level_two_input = QLineEdit()
        layout.addWidget(self.level_two_input)

        # Level THREE
        level_three_label = QLabel('Level THREE (Enter number of questions):')
        layout.addWidget(level_three_label)
        self.level_three_input = QLineEdit()
        layout.addWidget(self.level_three_input)

        startButton = QPushButton('Start Practice')
        startButton.clicked.connect(self.start_practice)
        layout.addWidget(startButton)

        backButton = QPushButton('Back')
        backButton.clicked.connect(self.back)
        layout.addWidget(backButton)

        self.setLayout(layout)

    def back(self):
        self.student_page = StudentPage()
        self.student_page.show()
        self.close()

    def start_practice(self):
        
        number_of_questions_one = int(self.level_one_input.text())
        number_of_questions_two = int(self.level_two_input.text())
        number_of_questions_three = int(self.level_three_input.text())

        # Get questions from database
        gq = GetQuestions()
        questions_level_one = gq.get_questions_from_db(1, number_of_questions_one)
        questions_level_two = gq.get_questions_from_db(2, number_of_questions_two)
        questions_level_three = gq.get_questions_from_db(3, number_of_questions_three) 
       
        msg = QMessageBox()
        msg.setWindowTitle("Practice Structure Submitted") 
        msg.setText("Close this to begin your assesment!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

        self.all_questions = questions_level_one + questions_level_two + questions_level_three
        
        self.question_page = QuestionsPage(self.all_questions)
        self.question_page.show()
        self.close()
        self.question_page.submitted.connect(self.show_practice_grades)
 
        
    @pyqtSlot()
    
    def show_practice_grades(self):
        #self.question_page.close()  # Close the QuestionsPage
        self.practice_grades_page = PracticeGradesPage(self.question_page.grades_summary)
        self.practice_grades_page.show()
        self.question_page.close()
         
class PracticeGradesPage(QWidget):
    def __init__(self, grades_summary):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle('Grades Page')
        layout = QVBoxLayout()

        self.grades_summary = QTextEdit()
        self.grades_summary.setReadOnly(True)
        self.grades_summary.setText("\n".join(grades_summary))
        layout.addWidget(self.grades_summary)

        backButton = QPushButton('Back')
        backButton.clicked.connect(self.back)
        layout.addWidget(backButton)

        self.setLayout(layout)

    def back(self):
        self.student_page = StudentPage()
        self.student_page.show()
        self.close()

class CSVPage(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800,600)
        self.setWindowTitle('CSV Page')
        self.fileName = ""
        layout = QVBoxLayout()

        uploadButton = QPushButton('Upload CSV File')
        uploadButton.clicked.connect(self.upload_csv)
        layout.addWidget(uploadButton)

        self.csv_preview = QTextEdit()
        self.csv_preview.setReadOnly(True)
        layout.addWidget(self.csv_preview)

        submitButton = QPushButton('Submit CSV File')
        submitButton.clicked.connect(self.submit_csv)
        layout.addWidget(submitButton)

        backButton = QPushButton('Back')
        backButton.clicked.connect(self.back)
        layout.addWidget(backButton)

        self.setLayout(layout)

    def back(self):
        self.admin_page = AdminPage()
        self.admin_page.show()
        self.close()

    def upload_csv(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Upload CSV File", "", "CSV Files (*.csv)", options=options)
        if self.fileName:
            with open(self.fileName, 'r') as file:
                csv_content = file.read()
                self.csv_preview.setText(csv_content)
            print("CSV File uploaded:", self.fileName)
    
    def submit_csv(self):
        ctb = csv_to_DB(self.fileName)
        ctb.insert_CSV()
        
class GradesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle('Grades Page')

        layout = QVBoxLayout()

        label = QLabel('Enter Assessment ID')
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.assessment_id_input = QLineEdit()
        layout.addWidget(self.assessment_id_input)

        buttonEnter = QPushButton('Enter')
        buttonEnter.clicked.connect(self.enter)
        layout.addWidget(buttonEnter)

        self.tableWidget = QTableWidget()
        layout.addWidget(self.tableWidget)

        backButton = QPushButton('Back')
        backButton.clicked.connect(self.back)
        layout.addWidget(backButton)

        self.setLayout(layout)

    def back(self):
        self.admin_page = AdminPage()
        self.admin_page.show()
        self.close()

    def enter(self):
        assessment_id = self.assessment_id_input.text()
        self.gg = GetGrades(assessment_id)
        self.display_grades(self.gg.get_grades())

    def display_grades(self, grades):
        self.tableWidget.setRowCount(len(grades))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['AssessmentID', 'StudentNumber', 'Grade'])
        
        for row, grade in enumerate(grades):
            for column, item in enumerate(grade):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))

if __name__ == "__main__": 
    
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())
