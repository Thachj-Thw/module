from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
import sys
from module import Path, Window
import emulator


path = Path(__file__)


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi(path.source.join("test", "test.ui"), self)
        main_win = Window.from_pyqt(self)
        self.ld = emulator.LDPlayer("d:/ldplayer/ldplayer4.0")
        em = self.ld.emulators[0].start(wait=False)
        child = Window(em.top_hwnd)
        child.set_window_position(0, 0)
        child.set_window_size(200, 150)
        child.set_enabled(False)
        main_win.attach_child(child)

    def closeEvent(self, event):
        self.ld.quit_all()
        self.ld.exit()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    sys.exit(app.exec_())
