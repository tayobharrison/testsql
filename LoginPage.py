import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLineEdit, QMessageBox, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSlot
from checkLogin import checkLogin
from StudentPage import StudentPage
from AdminPage import AdminPage

class LoginPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(885, 638)
        MainWindow.setMinimumSize(QtCore.QSize(885, 638))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Set up background label
        self.background_label = QtWidgets.QLabel(self.centralwidget)
        self.background_image = QtGui.QPixmap("/Users/tayob/Desktop/testsql/login_widgets/uct.png")
        self.background_label.setPixmap(self.background_image)
        self.background_label.setScaledContents(True)  # This ensures the image scales with the window
        self.background_label.resize(self.size())  # Initial resize to match the window size

        # Set up login box
        login_box = QtWidgets.QWidget(self.centralwidget)
        login_box.setStyleSheet("background-color: rgba(113, 120, 143, 150); border-radius: 10px; padding: 20px;")
        login_layout = QtWidgets.QVBoxLayout(login_box)

        # Add login text fields and input boxes
        self.create_label('user_id_label', "Username")
        login_layout.addWidget(self.user_id_label, 0, QtCore.Qt.AlignCenter)

        self.create_line_edit('user_id_input')
        login_layout.addWidget(self.user_id_input, 0, QtCore.Qt.AlignCenter)

        self.create_label('password_label', "Password")
        login_layout.addWidget(self.password_label, 0, QtCore.Qt.AlignCenter)

        self.create_line_edit('password_input')
        login_layout.addWidget(self.password_input, 0, QtCore.Qt.AlignCenter)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.check_login)

            # Create and add the UCT logo label
        self.logo_label = QtWidgets.QLabel(self.centralwidget)
        self.logo_pixmap = QtGui.QPixmap("/Users/tayob/Desktop/testsql/login_widgets/uct-logo.png") 
        self.logo_pixmap = self.logo_pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation) 
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setFixedSize(100,100)
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)
        
        # Create login button
        self.login_button = QtWidgets.QPushButton("Login", self.centralwidget)
        self.login_button.setObjectName("login_button")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(9, 0, 136);
                border: none;
                color: rgb(255, 255, 255);
                border-radius: 15px;
                padding: 8px 10px;
                font-size: 16pt;
            }
            QPushButton:hover {
                background-color: rgb(3, 0, 46);
            }
            QPushButton:pressed {
                background-color: #3b3b3b;
            }
        """)
        self.login_button.clicked.connect(self.check_login)
       

        # Center the login box and button
        vbox_centered = QVBoxLayout()
        vbox_centered.addStretch()  # Add stretchable space before the login box
        vbox_centered.addWidget(self.logo_label, 0, QtCore.Qt.AlignCenter) 
        vbox_centered.addWidget(login_box, 0, QtCore.Qt.AlignCenter)
        vbox_centered.addWidget(self.login_button, 0, QtCore.Qt.AlignCenter)  # Add login button directly below the login box
        vbox_centered.addStretch()  # Add stretchable space after the login box

        # Set up main layout for centering
        main_vbox = QVBoxLayout(self.centralwidget)
        main_vbox.setContentsMargins(0, 0, 0, 0)
        main_vbox.addLayout(vbox_centered)

        self.centralwidget.setLayout(main_vbox)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def create_line_edit(self, name, read_only=False):
        line_edit = QLineEdit(self.centralwidget)
        line_edit.setStyleSheet("""
            background-color: transparent;  /* Keep the background transparent */
            font: 14pt "Aptos";
            color: black;  /* Set text color to black */
            border: 2px solid #3b3b3b;  /* Add a black border */
            padding: 5px;  /* Add some padding for better appearance */
            border-radius: 5px;  /* Optional: Add rounded corners to the border */
        """)
        line_edit.setObjectName(name)
        line_edit.setReadOnly(read_only)
        line_edit.setFixedHeight(30)  # Set a fixed height to fit the text size
        setattr(self, name, line_edit)



    def create_label(self, name, text, font_size=16):
        label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Aptos")
        font.setPointSize(font_size)
        label.setFont(font)
        label.setObjectName(name)
        label.setText(text)
        label.setStyleSheet("color: #1d1d1d; background-color: transparent;")  # Set text color to black and make background transparent
        label.setFixedWidth(120)
        setattr(self, name, label)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def check_login(self):
        self.user_id = self.user_id_input.text()
        self.password = self.password_input.text()

        self.cl = checkLogin()
        self.stuNum = self.user_id

        user_role = self.cl.verify(self.user_id, self.password)

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

    def open_student_page(self):
        self.student_page = StudentPage(self.stuNum)
        self.student_page.show()
        self.student_page.backPressed.connect(self.show_login_page)
        self.close()

    @pyqtSlot()
    def show_login_page(self):
        self.show()
        self.user_id_input.clear()
        self.password_input.clear()

    def open_admin_page(self):
        self.admin_page = AdminPage()
        self.admin_page.show()
        self.admin_page.backPressed.connect(self.show_login_page)
        self.close()

    def resizeEvent(self, event):
        # Resize the background label to match the window size
        self.background_label.resize(self.size())
        # Optionally, you can rescale the pixmap to fit the new size, preserving aspect ratio
        self.background_label.setPixmap(self.background_image.scaled(self.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())
