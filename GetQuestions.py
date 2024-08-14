from mysql.connector import MySQLConnection
import mysql.connector
from PyQt5.QtWidgets import QApplication, QComboBox, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
import random

class GetQuestions():

    def __init__(self, lev = 0, no = 0):
        self.lev = lev
        self.no = no

    def get_questions_from_db(self, level, number_of_questions):

        self.lev = level
        self.no = number_of_questions

        config = {
            "host": "localhost",
            "user": "root",
            "password": "new_password",
            "database": "testSqlDB"
        }

        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        getQIDs = "SELECT id from testSqlDB.qnaforclassicmodels WHERE level = %s;"
        cursor.execute(getQIDs, (level,))
        qIDs = cursor.fetchall() #get all the qIDs of the specifed level question
        
        indexes = [] # the indexes of the qIDs data structure 
        
        for i in range(number_of_questions): # get specified amount of random questions
            num = random.randint(0, len(qIDs)-1) #random index in qIDs
    
            if num not in indexes:
                indexes.append(num) #indexes to get from qIDs
                print(indexes)
            
        qIDToUse = [] #the actual question ids to retrieve 
        
        for index in indexes:
            
            qID = qIDs[index][0]
            qIDToUse.append(qID)
            print("Question IDs:", qIDToUse)
        
        results = []
        
        for q in qIDToUse:
            
            query = "SELECT QUESTION, ANSWER FROM testSqlDB.qnaforclassicmodels WHERE id = %s;"
            cursor.execute(query, (q,))
            result = cursor.fetchone()
            results.append(result)
            
        cursor.close()
        connection.close()
        print(results[0][0])
        return results
        