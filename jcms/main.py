import time

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QPoint
import options,ui.resource


class main_ui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        uic.loadUi(r'.\ui\main_window.ui', self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.pushButton_install.clicked.connect(lambda: self.options(101))
        self.pushButton_activate.clicked.connect(lambda: self.options(102))
        self.pushButton_uninstall.clicked.connect(lambda: self.options(103))
        self.pushButton_deactivate.clicked.connect(lambda: self.options(104))
        self.pushButton_login.clicked.connect(self.login)

        self.pushButton_install.setVisible(False)
        self.pushButton_uninstall.setVisible(False)
        self.pushButton_deactivate.setVisible(False)
        self.pushButton_activate.setVisible(False)

        self.progressBar.setVisible(False)
        self.label_done.setVisible(False)

        self.offset = QPoint()
    def mousePressEvent(self, event):
        # 记录鼠标按下的初始位置
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        # 移动窗口位置
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def login(self):
        user_password = self.lineEdit.text()
        self.thread_login = options.login(user_password)
        self.thread_login.signal_login.connect(self.options)
        self.thread_login.start()


    def options(self, signal_login):
        if signal_login == '1':
            self.pushButton_login.setVisible(False)
            self.lineEdit.setVisible(False)
            self.progressBar.setVisible(True)

            self.subThread = options.install_studio(1)
            self.subThread.signal_progressBar.connect(self.set_progressBar)
            self.subThread.start()
        elif type(signal_login) == int:
            self.subThread = options.install_studio(signal_login)
            self.subThread.signal_progressBar.connect(self.set_progressBar)
            self.subThread.start()
        else:
            QtWidgets.QMessageBox.about(self, '登录提示', signal_login)


    def set_progressBar(self, progressbar_value):
        self.progressBar.setValue(progressbar_value)
        if progressbar_value == 100:
            time.sleep(3)
            self.progressBar.setVisible(False)
            self.label_done.setVisible(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = main_ui()
    main_window.show()
    app.exec_()