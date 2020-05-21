# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QtSnakeUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!

import sys

from PyQt5 import QtCore, QtGui, QtWidgets

stepX = 20
stepY = 20

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(685, 550)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.keyPressEvent = self.newkeyPressEvent
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gameField = QtWidgets.QGroupBox(self.centralwidget)
        self.gameField.setGeometry(QtCore.QRect(0, 0, 500, 500))
        self.gameField.setMinimumSize(QtCore.QSize(500, 500))
        self.gameField.setMaximumSize(QtCore.QSize(500, 500))
        self.gameField.setObjectName("gameField")
        self.gameField.setTitle("sdfsdf")
        self.gameField.setStyleSheet("background-color:#e0c31e; border: 0px dashed black;");
        self.label = QtWidgets.QLabel(self.gameField)
        self.label.setGeometry(QtCore.QRect(10, 10, 20, 20))
        self.label.setStyleSheet("background-image: url(img/snakeBody.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.goLeftButton = QtWidgets.QPushButton(self.centralwidget)
        self.goLeftButton.setGeometry(QtCore.QRect(520, 50, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.goLeftButton.setFont(font)
        self.goLeftButton.setObjectName("goLeftButton")
        self.goRightButton = QtWidgets.QPushButton(self.centralwidget)
        self.goRightButton.setGeometry(QtCore.QRect(620, 50, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.goRightButton.setFont(font)
        self.goRightButton.setObjectName("goRightButton")
        self.goDownButton = QtWidgets.QPushButton(self.centralwidget)
        self.goDownButton.setGeometry(QtCore.QRect(570, 50, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.goDownButton.setFont(font)
        self.goDownButton.setObjectName("goDownButton")
        self.goUpButton = QtWidgets.QPushButton(self.centralwidget)
        self.goUpButton.setGeometry(QtCore.QRect(570, 0, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.goUpButton.setFont(font)
        self.goUpButton.setObjectName("goUpButton")

        # Привязываем события к кнопкам
        self.goLeftButton.clicked.connect(self.clickedLeft)
        self.goRightButton.clicked.connect(self.clickedRight)
        self.goUpButton.clicked.connect(self.clickedUp)
        self.goDownButton.clicked.connect(self.clickedDown)
        # чтобы данные кнопки не перехватывали фокус нажатия клавиш-стрелок
        self.goLeftButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.goRightButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.goUpButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.goDownButton.setFocusPolicy(QtCore.Qt.NoFocus)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 685, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.gameField.setTitle(_translate("MainWindow", "gameField"))
        self.goLeftButton.setText(_translate("MainWindow", "←"))
        self.goRightButton.setText(_translate("MainWindow", "→"))
        self.goDownButton.setText(_translate("MainWindow", "↓"))
        self.goUpButton.setText(_translate("MainWindow", "↑"))

    def clickedUp(self):
        self.label.move(self.label.pos().x(), self.label.pos().y() - stepY)

    def clickedDown(self):
        self.label.move(self.label.pos().x(), self.label.pos().y() + stepY)

    def clickedLeft(self):
        self.label.move(self.label.pos().x() - stepX, self.label.pos().y())

    def clickedRight(self):
        self.label.move(self.label.pos().x() + stepX, self.label.pos().y())

    def newkeyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            self.clickedLeft()
        elif event.key() == QtCore.Qt.Key_Right:
            self.clickedRight()
        elif event.key() == QtCore.Qt.Key_Up:
            self.clickedUp()
        elif event.key() == QtCore.Qt.Key_Down:
            self.clickedDown()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(win)
    win.show()
    sys.exit(app.exec_())
