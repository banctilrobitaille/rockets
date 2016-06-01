import PyQt4
import time


class SlidingMessage(PyQt4.QtGui.QFrame):
    def __init__(self, message, parent):
        super(SlidingMessage, self).__init__(parent)

        self.__layout = PyQt4.QtGui.QHBoxLayout()

        self.__text = PyQt4.QtGui.QLabel(message)
        self.__text.setObjectName("text")
        self.__text.setAlignment(PyQt4.QtCore.Qt.AlignCenter)
        self.__text.setStyleSheet("QFrame#text {color: white;}")

        self.icon = PyQt4.QtGui.QLabel()
        self.icon.setAlignment(PyQt4.QtCore.Qt.AlignLeft)
        self.icon.setSizePolicy(PyQt4.QtGui.QSizePolicy.Expanding, PyQt4.QtGui.QSizePolicy.Expanding)
        self.icon.setMinimumSize(32, 32)

        self.__iconLabel = PyQt4.QtGui.QLabel()
        self.__iconLabel.setAlignment(PyQt4.QtCore.Qt.AlignRight)
        self.__iconLabel.setSizePolicy(PyQt4.QtGui.QSizePolicy.Expanding, PyQt4.QtGui.QSizePolicy.Expanding)
        self.__iconLabel.setMinimumSize(32, 32)
        self.__iconLabel.setPixmap(PyQt4.QtGui.QPixmap('./Image_Files/SlidingMessage/close.png'))

        self.__layout.addWidget(self.icon)
        self.__layout.addWidget(self.__text)
        self.__layout.addWidget(self.__iconLabel)

        self.setLayout(self.__layout)
        self.setAutoFillBackground(True)
        self.setGeometry(300, 0, 300, 0)

        self.__revealAnimation = PyQt4.QtCore.QPropertyAnimation(self, "geometry")
        self.__revealAnimation.setDuration(250)
        self.__revealAnimation.setStartValue(PyQt4.QtCore.QRect(1000, -105, 500, 105))
        self.__revealAnimation.setEndValue(PyQt4.QtCore.QRect(1000, 0, 500, 105))

        self.__hideAnimation = PyQt4.QtCore.QPropertyAnimation(self, "geometry")
        self.__hideAnimation.setDuration(100)
        self.__hideAnimation.setStartValue(PyQt4.QtCore.QRect(1000, 0, 500, 105))
        self.__hideAnimation.setEndValue(PyQt4.QtCore.QRect(1000, -105, 500, 105))
        self.show()

        self.mousePressEvent = self.hide

    def reveal(self):
        self.__revealAnimation.start()

    def hide(self, event):
        self.__hideAnimation.start()


class ErrorSlidingMessage(SlidingMessage):
    def __init__(self, message, parent):
        super(ErrorSlidingMessage, self).__init__(message, parent)
        self.icon.setPixmap(PyQt4.QtGui.QPixmap('./Image_Files/SlidingMessage/error.png'))
        self.setStyleSheet("QFrame {background : rgba(207,0,15,230)}"
                           "QFrame QLabel {background : rgba(207,0,15,0);padding: 10px;}")


class NotificationSlidingMessage(SlidingMessage):
    def __init__(self, message, parent):
        super(NotificationSlidingMessage, self).__init__(message, parent)
        self.icon.setPixmap(PyQt4.QtGui.QPixmap('./Image_Files/SlidingMessage/information.png'))
        self.setStyleSheet("QFrame {background : rgba(30,139,195,230)}"
                           "QFrame QLabel {background : rgba(30,139,195,0);padding: 10px;}")


class SuccessSlidingMessage(SlidingMessage):
    def __init__(self, message, parent):
        super(SuccessSlidingMessage, self).__init__(message, parent)
        self.icon.setPixmap(PyQt4.QtGui.QPixmap('./Image_Files/SlidingMessage/success.png'))
        self.setStyleSheet("QFrame {background : rgba(0,177,106,230)}"
                           "QFrame QLabel {background : rgba(30,139,195,0);padding: 10px;}")
