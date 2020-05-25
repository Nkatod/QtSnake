# -*- coding: utf-8 -*-

import sys
import traceback
import time
import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from random import randint

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

class WorkerSignals(QtCore.QObject):
    '''
    Defines the signals available from a running worker thread.
    Supported signals are:
    finished
        No data
    error
        `tuple` (exctype, value, traceback.format_exc() )
    result
        `object` data returned from processing, anything
    progress
        `int` indicating % progress
    '''
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(tuple)
    result = QtCore.pyqtSignal(object)
    progress = QtCore.pyqtSignal(int)

class Worker(QtCore.QRunnable):
    '''
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    '''
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress
        logging.debug('Worker init')

    @QtCore.pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        # Retrieve args/kwargs here; and fire processing using them
        logging.debug('Worker start')
        try:
            result = self.fn.run(*self.args, **self.kwargs)
        except:
            logging.debug('Worker except')
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

class GameEngine:
    def __init__(self, *args, **kwargs):
        self.crash = False
        self.player = None
        self.food = None
        self.score = 0
        self.stepX = 20
        self.stepY = 20
        self.game_width = 500
        self.game_height = 500
        self.MainWindow = None
        self.stopFlag = False
        for arg, val in kwargs.items():
            if arg == 'MainWindow':
                self.MainWindow = val

    def initPlayer(self):
        self.player = Player(self)
        self.food = Food()
        self.food.food_coord(self, self.player)


    def run(self, progress_callback):
        self.initPlayer()
        self.MainWindow.display(self)
        self.MainWindow.labelTimer.setText("Food: %d" % self.player.food)
        while not self.crash and not self.stopFlag:
            if self.stopFlag:
                break
            self.player.do_move(self.player.x, self.player.y, self, self.food)
            self.MainWindow.labelTimer.setText("Food: %d" % self.player.food)
            self.MainWindow.display(self)
            time.sleep(0.5)
        if self.stopFlag:
            return 'Game stopped'

        return 'Game end'

class Player():
    def __init__(self, game):
        x = 0.3 * game.game_width
        y = 0.5 * game.game_height
        self.x = x - x % game.stepX
        self.y = y - y % game.stepY
        self.position = []
        self.position.append([self.x, self.y])
        self.food = 1
        self.eaten = False
        self.x_change = 20
        self.y_change = 0

    def update_position(self, x, y):
        if self.position[-1][0] != x or self.position[-1][1] != y:
            if self.food > 1:
                for i in range(0, self.food - 1):
                    self.position[i][0], self.position[i][1] = self.position[i + 1]
            self.position[-1][0] = x
            self.position[-1][1] = y

    def do_move(self, x, y, game, food):
        if self.eaten:
            self.position.append([self.x, self.y])
            self.eaten = False
            self.food = self.food + 1
        self.x = x + self.x_change
        self.y = y + self.y_change
        if self.x < 20 or self.x > game.game_width - 40 \
                or self.y < 20 \
                or self.y > game.game_height - 40 \
                or [self.x, self.y] in self.position:
            game.crash = True
        eat(self, food, game)
        self.update_position(self.x, self.y)

    def display_player(self, x, y, food, game):
        #Чистим предыдущую змейку
        for label in game.MainWindow.arraySnakeBody:
            label.move(1000, 1000) #убираем за границы экрана
        self.position[-1][0] = x
        self.position[-1][1] = y
        game.MainWindow.arraySnakeBody[0].move(self.position[-1][0], self.position[-1][1])
        game.MainWindow.arraySnakeBody[0].setStyleSheet("background-color:#0057e7;")

        if not game.crash:
            for i in range(food):
                x_temp, y_temp = self.position[len(self.position) - 1 - i]
                game.MainWindow.arraySnakeBody[i].move(x_temp, y_temp)


class Food():
    def __init__(self):
        self.x_food = 0
        self.y_food = 0

    def food_coord(self, game, player):
        x_rand = randint(20, game.game_width - 40)
        self.x_food = x_rand - x_rand % game.stepX
        y_rand = randint(20, game.game_height - 40)
        self.y_food = y_rand - y_rand % game.stepY
        if [self.x_food, self.y_food] not in player.position:
            return self.x_food, self.y_food
        else:
            self.food_coord(game, player)

    def display_food(self, game):
        for label in game.MainWindow.arrayFood:
            label.move(1000, 1000) #убираем за границы экрана
        game.MainWindow.arrayFood[0].move(self.x_food, self.y_food)


def eat(player, food, game):
    if player.x == food.x_food and player.y == food.y_food:
        food.food_coord(game, player)
        player.eaten = True
        game.score = game.score + 1


class Ui_MainWindow(object):
    def __init__(self, MainWindow):
        self.counter = 0
        self.game = None
        self.arraySnakeBody = []
        self.arrayFood = []
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
        self.gameField.setStyleSheet("background-color:#e0c31e; border: 0px dashed black;")
        self.createObjectPool()
        self.goLeftButton = QtWidgets.QPushButton(self.centralwidget)
        self.goLeftButton.setGeometry(QtCore.QRect(520, 50, 50, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.goLeftButton.setFont(font)
        self.goLeftButton.setObjectName("goLeftButton")
        self.goRightButton = QtWidgets.QPushButton(self.centralwidget)
        self.goRightButton.setGeometry(QtCore.QRect(620, 50, 50, 50))
        self.goRightButton.setFont(font)
        self.goRightButton.setObjectName("goRightButton")
        self.goDownButton = QtWidgets.QPushButton(self.centralwidget)
        self.goDownButton.setGeometry(QtCore.QRect(570, 50, 50, 50))
        self.goDownButton.setFont(font)
        self.goDownButton.setObjectName("goDownButton")
        self.goUpButton = QtWidgets.QPushButton(self.centralwidget)
        self.goUpButton.setGeometry(QtCore.QRect(570, 0, 50, 50))
        self.goUpButton.setFont(font)
        self.goUpButton.setObjectName("goUpButton")

        self.newGameButton = QtWidgets.QPushButton(self.centralwidget)
        self.newGameButton.setGeometry(QtCore.QRect(570, 100, 100, 50))
        self.newGameButton.setFont(font)
        self.newGameButton.setObjectName("newGameButton")

        # Привязываем события к кнопкам
        self.goLeftButton.clicked.connect(self.clickedLeft)
        self.goRightButton.clicked.connect(self.clickedRight)
        self.goUpButton.clicked.connect(self.clickedUp)
        self.goDownButton.clicked.connect(self.clickedDown)
        self.newGameButton.clicked.connect(self.clickedNewGame)
        # чтобы данные кнопки не перехватывали фокус нажатия клавиш-стрелок
        self.goLeftButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.goRightButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.goUpButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.goDownButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.newGameButton.setFocusPolicy(QtCore.Qt.NoFocus)

        self.labelTimer = QtWidgets.QLabel(self.centralwidget)
        self.labelTimer.setGeometry(QtCore.QRect(550, 300, 100, 20))
        self.labelTimer.setText("")
        self.labelTimer.setObjectName("labelTimer")
        # self.DangerButton = QtWidgets.QPushButton(self.centralwidget)
        # self.DangerButton.setGeometry(QtCore.QRect(550, 400, 50, 50))
        # self.DangerButton.pressed.connect(self.oh_no)
        # self.DangerButton.setFocusPolicy(QtCore.Qt.NoFocus)

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

        self.threadpool = QtCore.QThreadPool()
        self.gameMainThread = None
        # self.timer = QTimer()
        # self.timer.setInterval(1000)
        # self.timer.timeout.connect(self.recurring_timer)
        # self.timer.start()

    def createObjectPool(self):
        for i in range(100):
            label = QtWidgets.QLabel(self.gameField)
            label.setGeometry(QtCore.QRect(1000, 1000, 20, 20))
            label.setStyleSheet("background-color:#008744;")
            label.setText("")
            label.setObjectName("label"+str(i))
            self.arraySnakeBody.append(label)

        for i in range(10):
            label = QtWidgets.QLabel(self.gameField)
            label.setGeometry(QtCore.QRect(1000, 1000, 20, 20))
            label.setStyleSheet("background-color:#90ee90;")
            label.setText("")
            label.setObjectName("labelFood"+str(i))
            self.arrayFood.append(label)


    def display(self, game):
        x = game.player.position[-1][0]
        y = game.player.position[-1][1]
        game.player.display_player(x, y, game.player.food, game)
        game.food.display_food(game)

    def setupUi(self, MainWindow):
        MainWindow.setStatusBar(self.statusbar)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.gameField.setTitle(_translate("MainWindow", " "))
        self.goLeftButton.setText(_translate("MainWindow", "←"))
        self.goRightButton.setText(_translate("MainWindow", "→"))
        self.goDownButton.setText(_translate("MainWindow", "↓"))
        self.goUpButton.setText(_translate("MainWindow", "↑"))
        self.newGameButton.setText(_translate("MainWindow", "New game"))
        #self.DangerButton.setText(_translate("MainWindow", "Danger"))


    def clickedUp(self):
        # self.label.move(self.label.pos().x(), self.label.pos().y() - self.game.stepY)
        self.game.player.x_change = 0
        self.game.player.y_change = -self.game.stepY

    def clickedDown(self):
        # self.label.move(self.label.pos().x(), self.label.pos().y() + self.game.stepY)
        self.game.player.x_change = 0
        self.game.player.y_change = self.game.stepY

    def clickedLeft(self):
        # self.label.move(self.label.pos().x() - self.game.stepX, self.label.pos().y())
        self.game.player.x_change = -self.game.stepX
        self.game.player.y_change = 0

    def clickedRight(self):
        # self.label.move(self.label.pos().x() + self.game.stepX, self.label.pos().y())
        self.game.player.x_change = self.game.stepX
        self.game.player.y_change = 0

    def clickedNewGame(self):
        if self.gameMainThread != None:
            self.game.stopFlag = True
            time.sleep(1)
        self.game = GameEngine(MainWindow = self)
        self.gameMainThread = Worker(self.game) #Any other args, kwargs are passed to the run function
        self.gameMainThread.signals.result.connect(self.print_output)
        self.gameMainThread.signals.finished.connect(self.thread_complete)
        self.gameMainThread.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(self.gameMainThread)

    def newkeyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            self.clickedLeft()
        elif event.key() == QtCore.Qt.Key_Right:
            self.clickedRight()
        elif event.key() == QtCore.Qt.Key_Up:
            self.clickedUp()
        elif event.key() == QtCore.Qt.Key_Down:
            self.clickedDown()

    def oh_no(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn) #Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)

    def recurring_timer(self):
        self.counter +=1
        self.labelTimer.setText("Counter: %d" % self.counter)

    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):
        for n in range(0, 5):
            self.recurring_timer()
            time.sleep(1)
            progress_callback.emit(n*100/4)
        return "Done."

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # app = QtWidgets.QApplication.instance()
    # if app is None:
    #     app = QtWidgets.QApplication(sys.argv)
    # else:
    #     print('QApplication instance already exists: %s' % str(app))
    win = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(win)
    #ui.setupUi(win)
    win.show()
    sys.exit(app.exec_())
