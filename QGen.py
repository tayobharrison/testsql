import mysql.connector
import random
import string
class QGen:

    def _init_(self, db_config):
        self.db_config = db_config
        self.db_config = {
        "host": "localhost",
        "user": "root",
        "password": "new_password",
        "database": "testSQLDB"
        }

    @staticmethod
    def ireplace(old, new, text):
        # This method will perform a case-insensitive replacement of 'old' with 'new' in 'text'
        index_l = 0
        while index_l != -1:
            index_l = text.lower().find(old.lower(), index_l)
            if index_l == -1:
                break  # exit the loop if 'old' is not found
            text = text[:index_l] + new + text[index_l + len(old):]
            index_l += len(new)  # move to the next occurrence
        return text

    def quesGen(self):
        
        
        
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor()

        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall() if table[0].lower() != 'qnaforclassicmodels']

        table_columns = {}
        for table in tables:
            cursor.execute(f"SHOW COLUMNS FROM {table}")
            columns = cursor.fetchall()
            table_columns[table.lower()] = {column[0].lower() for column in columns}

        cursor.execute("SELECT * FROM qnaforclassicmodels WHERE level = 1")
        rows = cursor.fetchall()

        for row in rows:
            if row:
                question_to_edit = str(row[1])
                corres_ans = str(row[2])

                for orig_table in tables:
                    lower_orig_table = orig_table.lower()
                    if lower_orig_table in question_to_edit.lower():
                        for repl_table in tables:
                            if repl_table.lower() != lower_orig_table:
                                new_question = self.ireplace(orig_table, repl_table.upper(), question_to_edit)
                                new_answer = self.ireplace(orig_table, repl_table.upper(), corres_ans)

                                for orig_column in table_columns[lower_orig_table]:
                                    if orig_column in new_question.lower():
                                        for repl_column in table_columns[repl_table.lower()]:
                                            if repl_column != orig_column:
                                                final_question = self.ireplace(orig_column, repl_column.upper(),
                                                                               new_question)
                                                final_answer = self.ireplace(orig_column, repl_column.upper(),
                                                                             new_answer)
                                                print('Question:', final_question)
                                                print('Answer:', final_answer)

                                                self.append_to_qna_table(final_question, final_answer, 1)

        cursor.close()
        connection.close()

        return table_columns

    def set_auto_increment_start(self):
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT MAX(id) FROM qnaforclassicmodels;")
            max_id = cursor.fetchone()[0]
            cursor.execute(f"ALTER TABLE qnaforclassicmodels AUTO_INCREMENT = {max_id + 1};")
            cursor.execute("ALTER TABLE qnaforclassicmodels MODIFY id INT AUTO_INCREMENT;")
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()
    

    def append_to_qna_table(self, question, answer, level):
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor()

        insert_sql = """INSERT INTO qnaforclassicmodels (question, answer, level)
                        VALUES (%s, %s, %s)"""
        values = (question, answer, level)

        try:
            cursor.execute(insert_sql, values)
            connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()




# for _ in range(10):
#     question, sql_query, level = qgen.generate_dynamic_question(table_columns)
#     print(f"Generated Question: {question}")
#     print(f"Corresponding SQL: {sql_query}")
#     qgen.append_to_qna_table(question, sql_query, level)