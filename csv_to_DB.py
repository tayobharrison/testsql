import pandas as pd
import mysql.connector
from PyQt5.QtWidgets import QApplication, QSizePolicy, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt

class csv_to_DB(): 
    
    def __init__(self, fileName):

        self.fileName = fileName
        self.dbName = "testSqlDB"
        self.tableName = "qnaforclassicmodels"

    def insert_CSV(self):
    
        # Read CSV data into a DataFrame
        df = pd.read_csv(self.fileName, delimiter=";")

        db_config = {
        "host": "localhost",
        "user": "root",
        "password": "new_password",
        "database": "testSqlDB"
        }

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        truncate_query = "TRUNCATE TABLE qnaforclassicmodels"
        cursor.execute(truncate_query)
        
        print(df.columns)
        print(df.head())

        

        # Adding an index column named 'id' to the DataFrame
        df.reset_index(inplace=True, drop=False)
        df.rename(columns={'index': 'id'}, inplace=True)


        df = df[['id', 'QUESTION', 'ANSWER', 'LEVEL']]

        for _, row in df.iterrows():
            #column_names = ', '.join([f'`{col}`' for col in df.columns])  # Use backticks around column names
            #placeholders = ', '.join(['%s'] * len(df.columns))
            insert_query = f"INSERT into`qnaforclassicmodels` (id, question, answer, level) VALUES (%s, %s, %s, %s)"

            cursor.execute(insert_query, tuple(row))

        # Commit the changes and close the cursor and connection
        connection.commit()
        cursor.close()
        connection.close()
        
        msg = QMessageBox()
        msg.setWindowTitle("CSV File Submitted")
        msg.setText("The CSV file has been successfully submitted!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

