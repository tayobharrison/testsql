from mysql.connector import MySQLConnection
import mysql.connector
from PyQt5.QtWidgets import QApplication, QComboBox, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt

class GetGrades():
    
    def __init__ (self, assessmentID=None):
        self.assessmentID = assessmentID
        self.config = {
            "host" :"localhost",
            "user": "root",
            "password" : "new_password",
            "database": "admin"
        }

            
        self.connection = mysql.connector.connect(**self.config)
    
    def get_grades(self):

        self.cursor = self.connection.cursor()
        query = "SELECT userID, assessment_code, grade FROM results WHERE assessment_code = %s GROUP BY userID, assessment_code, grade;"  
        self.cursor.execute(query, (self.assessmentID,))
        result = self.cursor.fetchall()
        self.connection.close()
        return result
    
    def assessment_exists(self, assessment_code):
        self.cursor = self.connection.cursor()
        query = "SELECT COUNT(*) FROM assessments WHERE assessment_code = %s"
        self.cursor.execute(query, (assessment_code,))
        result = self.cursor.fetchone()
        self.cursor.close()
        return result[0] > 0  # True if the assessment code exists, False otherwise

    def results_exist(self, assessment_code):
        self.cursor = self.connection.cursor()
        query = "SELECT COUNT(*) FROM results WHERE assessment_code = %s"
        self.cursor.execute(query, (assessment_code,))
        result = self.cursor.fetchone()
        self.cursor.close()
        return result[0] > 0  # True if results exist, False otherwise
    
    def alreadyTaken(self, stuNum, code):
        self.cursor = self.connection.cursor()
        query = "SELECT COUNT(*) FROM results WHERE userID = %s and assessment_code = %s"
        self.cursor.execute(query, (stuNum,code))
        result = self.cursor.fetchone()
        self.cursor.close()
        return result[0] > 0  # True if results exist, False otherwise
        