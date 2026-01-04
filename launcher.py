from PyQt5 import QtCore, QtGui, QtWidgets
from main import Main

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)
        MainWindow.setStyleSheet("background-color: rgb(36, 31, 49);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.play_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_button.setGeometry(QtCore.QRect(560, 410, 191, 51))
        self.play_button.setStyleSheet(
            "color: rgb(255, 255, 255);\n"
            "border-radius: 10px;\n"
            "border: 1px solid rgb(255, 255, 255);"
        )
        self.play_button.setObjectName("play_button")
        self.play_button.clicked.connect(self.start_game)

        self.version_label = QtWidgets.QLabel(self.centralwidget)
        self.version_label.setGeometry(QtCore.QRect(30, 350, 341, 21))
        self.version_label.setStyleSheet(
            "background-color: rgb(36, 31, 49);\n"
            "border: 1px solid;\n"
            "border-bottom: 0px;\n"
            "border-radius: 10px;"
        )
        self.version_label.setObjectName("version_label")

        self.info_label = QtWidgets.QLabel(self.centralwidget)
        self.info_label.setGeometry(QtCore.QRect(30, 370, 341, 101))
        self.info_label.setStyleSheet(
            "background-color: rgb(36, 31, 49);\n"
            "border: 1px solid ;\n"
            "border-radius: 10px;"
        )
        self.info_label.setObjectName("info_label")

        self.update_info_label = QtWidgets.QLabel(self.centralwidget)
        self.update_info_label.setGeometry(QtCore.QRect(130, 380, 231, 81))
        self.update_info_label.setStyleSheet(
            "border: 1px solid rgb(154, 153, 150);\n"
            "border-radius: 25px;\n"
            "border-right: 0px;\n"
            "color: rgb(153, 193, 241);"
        )
        self.update_info_label.setObjectName("update_info_label")

        self.nasroiki = QtWidgets.QPushButton(self.centralwidget)
        self.nasroiki.setGeometry(QtCore.QRect(760, 10, 31, 31))
        self.nasroiki.setStyleSheet(
            "border: 1px solid rgb(154, 153, 150);\n"
            "border-radius: 15px;\n"
            "color: rgb(153, 193, 241);"
        )
        self.nasroiki.setText("")
        self.nasroiki.setObjectName("nasroiki")

        self.sopport = QtWidgets.QPushButton(self.centralwidget)
        self.sopport.setGeometry(QtCore.QRect(760, 50, 31, 31))
        self.sopport.setStyleSheet(
            "border: 1px solid rgb(154, 153, 150);\n"
            "border-radius: 15px;\n"
            "color: rgb(153, 193, 241);"
        )
        self.sopport.setText("")
        self.sopport.setObjectName("sopport")

        self.blog = QtWidgets.QPushButton(self.centralwidget)
        self.blog.setGeometry(QtCore.QRect(760, 90, 31, 31))
        self.blog.setStyleSheet(
            "border: 1px solid rgb(154, 153, 150);\n"
            "border-radius: 15px;\n"
            "color: rgb(153, 193, 241);"
        )
        self.blog.setText("")
        self.blog.setObjectName("blog")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Endura2"))
        self.play_button.setText(_translate("MainWindow", "PLAY"))
        self.version_label.setText(
            _translate(
                "MainWindow",
                '<html><head/><body><p align="center"><span style=" color:#ffffff;">Версия игры: 0</span></p></body></html>'
            )
        )
        self.info_label.setText(
            _translate(
                "MainWindow",
                "<html><head/><body><p><span style=\" color:#ffffff;\">О обновление:</span></p></body></html>"
            )
        )
        self.update_info_label.setText(_translate("MainWindow", "text texttext text etxt text"))

    def start_game(self):
        self.game = Main()
        self.game.run()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
