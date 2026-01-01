from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1267, 721)
        MainWindow.setStyleSheet("background-color: rgba(0, 0, 0, 203);")
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.play_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_button.setGeometry(QtCore.QRect(890, 610, 281, 61))
        self.play_button.setStyleSheet("background-color: rgba(51, 16, 96, 166);\n"
"border-radius: 20px;\n"
"font-size:30px;\n"
"border-color: rgb(129, 61, 156);\n"
"\n"
"\n"
"")
        self.play_button.setObjectName("play_button")
        self.left_menu = QtWidgets.QLabel(self.centralwidget)
        self.left_menu.setGeometry(QtCore.QRect(1210, 0, 71, 721))
        self.left_menu.setStyleSheet("background-color: rgba(51, 16, 96, 166);\n"
"border-radius: 20px;")
        self.left_menu.setText("")
        self.left_menu.setObjectName("left_menu")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1220, 10, 51, 51))
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(1220, 70, 51, 51))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(1220, 130, 51, 51))
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(1220, 190, 51, 51))
        self.pushButton_5.setText("")
        self.pushButton_5.setObjectName("pushButton_5")
        self.game = QtWidgets.QLabel(self.centralwidget)
        self.game.setGeometry(QtCore.QRect(-10, 280, 201, 41))
        self.game.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);\n"
"padding: 10px;\n"
"padding-left:60px;\n"
"border-radius:20px;")
        self.game.setObjectName("game")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.play_button.setText(_translate("MainWindow", "PLAY"))
        self.game.setText(_translate("MainWindow", "Endura2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
