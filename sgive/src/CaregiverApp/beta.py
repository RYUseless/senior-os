import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMenu


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        super().__init__(parent)

        self.resolutionHeight = QApplication.desktop().screenGeometry().height()
        self.resolutionWidth = QApplication.desktop().screenGeometry().width()
        appHeight = (int)(self.resolutionHeight * 0.5)  # APPHEIGHT value
        appWidth = (int)(self.resolutionWidth * 0.5)  # APPWIDTH value
        self.setWindowTitle("Gugl from wish!")
        self.setGeometry(self.resolutionWidth // 2 - appWidth // 2, self.resolutionHeight // 2 - appHeight // 2, appWidth, appHeight)  #(xpos,ypos,width,height)
        self.showMaximized()
        self._createMenuBar()

    def _createMenuBar(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        # Creating menus using a title
        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&Help")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())