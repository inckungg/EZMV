import sys
import EZMV
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # creating main widget window
        self.main_widget = MainWidget(parent=self)
        self.setCentralWidget(self.main_widget)
        self.setGeometry(100, 100, 405, 608)
        self.setWindowTitle(f"EZMV Highlight")
        # filling up a menu bar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)  # MacOS
        # File menu
        file_menu = menubar.addMenu("Menu")

        Contact_menu = QtWidgets.QMenu("Contact", self)
        people1_con = QtWidgets.QMenu("INC", self)
        people2_con = QtWidgets.QMenu("PLEUM", self)
        people1_info = QtWidgets.QAction(
            QtGui.QIcon("Photo/FB-icon.png"), "FB: Inc'z Ronnakrit", self
        )
        people1_info2 = QtWidgets.QAction(
            QtGui.QIcon("Photo/TW-icon.png"), "TW: @tornadozebra1", self
        )
        people1_info3 = QtWidgets.QAction(
            QtGui.QIcon("Photo/Tel-icon.png"), "Tel: 094-543-5432", self
        )
        people2_info = QtWidgets.QAction(
            QtGui.QIcon("Photo/FB-icon.png"), "FB: Pleum Pawarut", self
        )
        people2_info2 = QtWidgets.QAction(
            QtGui.QIcon("Photo/TW-icon.png"), "TW: ", self
        )
        people2_info3 = QtWidgets.QAction(
            QtGui.QIcon("Photo/Tel-icon.png"), "Tel: 080-753-7444", self
        )

        people1_con.addAction(people1_info)
        people1_con.addAction(people1_info2)
        people1_con.addAction(people1_info3)
        people2_con.addAction(people2_info)
        people2_con.addAction(people2_info2)
        people2_con.addAction(people2_info3)

        Contact_menu.addMenu(people1_con)
        Contact_menu.addMenu(people2_con)

        exit_act = QtWidgets.QAction(QtGui.QIcon("Photo/app-icon.png"), "Exit", self)
        exit_act.setShortcut("Ctrl+Q")
        exit_act.setStatusTip("Exit application")
        exit_act.triggered.connect(QtWidgets.QApplication.instance().quit)

        file_menu.addMenu(Contact_menu)
        file_menu.addAction(exit_act)

        oImage = QImage("Photo/ezmv-bg.png")
        sImage = oImage.scaled(QSize(405, 608))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # create and set layout to place widgets
        url_text = QtWidgets.QLabel("URL")
        url_text.setStyleSheet("color: white;")
        url_text.setFont(QFont("Cloud-Bold", 14))
        proceed_btn = QtWidgets.QPushButton("Proceed", self)
        proceed_btn.setStyleSheet(
            "QPushButton {border-radius: 5 ; border: 1px solid white ; color: white;}"
            "QPushButton:pressed {border-radius: 5 ; border: 1px solid grey ; color: grey;}"
        )
        proceed_btn.setFont(QFont("Cloud-Bold", 11))
        proceed_btn.clicked.connect(lambda: self.proceed(urlEdit.text()))

        urlEdit = QtWidgets.QLineEdit()
        urlEdit.setStyleSheet(
            "QLineEdit {  border: 2px solid white;" "border-radius: 5px;}"
        )

        Hlayout = QtWidgets.QHBoxLayout()
        Hlayout.addWidget(url_text)
        Hlayout.addWidget(urlEdit)

        Hlayout2 = QtWidgets.QHBoxLayout()
        Hlayout2.addStretch()
        Hlayout2.addWidget(proceed_btn)
        Hlayout2.addStretch()

        Hlayout3 = QtWidgets.QHBoxLayout()
        self.b1 = QRadioButton("Magic Cut")
        Hlayout3.addWidget(self.b1)
        self.b1.setStyleSheet("color: white;")
        self.b1.setFont(QFont("Cloud-Bold", 10))

        self.b2 = QRadioButton("Color Palette")
        Hlayout3.addWidget(self.b2)
        self.b2.setStyleSheet("color: white;")
        self.b2.setFont(QFont("Cloud-Bold", 10))

        ezmv_icon = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap("Photo/ezmvLOGO.png")
        ezmv_icon.setPixmap(pixmap)

        Vlayout = QtWidgets.QVBoxLayout()
        Vlayout.addWidget(ezmv_icon)
        Vlayout.addLayout(Hlayout)
        Vlayout.addLayout(Hlayout3)
        Vlayout.addLayout(Hlayout2)
        Vlayout.setContentsMargins(100, 100, 90, 200)

        self.setLayout(Vlayout)

    def togglecheck(self):
        sender = self.sender()
        if sender.text("Magic Cut"):
            self.b1.setChecked(True)
            self.b2.setChecked(False)
        elif sender.text("Color Palette"):
            self.b2.setChecked(True)
            self.b1.setChecked(False)

    def proceed(self, URL):
        if URL == "":
            print("Provide URL First")
        else:
            pass
        if self.b1.isChecked():
            if URL == "":
                print("Provide URL First")
            else:
                EZMV.magic_cut(URL)
        elif self.b2.isChecked():
            if URL == "":
                print("Provide URL First")
            else:
                EZMV.color_palette(URL)
        else:
            print("Select Option first.")


def main():
    app = QtWidgets.QApplication(sys.argv)
    # creating main window
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    proceed_status = False
    received_url = None
    main()