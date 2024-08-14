from PyQt5.QtWidgets import QApplication, QComboBox, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
import mysql
from mysql.connector import MySQLConnection
import mysql.connector

class checkLogin():
     

    def __init__(self, userID=None, password=None):
          self.userID = userID
          self.password = password
          

    def verify(self, uID, pw):
            self.userID = uID
            self.password = pw

            # Here you can check the user_id and password against the database
            # If the user_id and password are correct, you can open the student or admin page based on role
            user_role = self.getUserRole(self.userID, self.password)

            return user_role
        
    def studentNum(self):
        return self.userID

    def getUserRole(self, user_id, password):
        config = {
            "host": "localhost",
            "user": "root",
            "password": "new_password",
            "database": "admin"
        }

        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        query = "SELECT userRole FROM userDetails WHERE userID = %s AND userPassword = %s"
        cursor.execute(query, (user_id, password))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result:
            return result[0]
        else:
            return -1