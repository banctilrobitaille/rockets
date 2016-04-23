import PyQt4
import time

class SlidingMessage(PyQt4.QtGui.QFrame):

    def __init__(self, message, parent):
        super(SlidingMessage, self).__init__(parent)

        self.layout = PyQt4.QtGui.QHBoxLayout()
        self.text = PyQt4.QtGui.QLabel(message)
        self.text.setObjectName("text")
        self.text.setAlignment(PyQt4.QtCore.Qt.AlignCenter)
        self.text.setStyleSheet("QFrame#text {color: white;}")
        self.icon = PyQt4.QtGui.QLabel()
        self.icon.setAlignment(PyQt4.QtCore.Qt.AlignLeft)
        self.icon.setSizePolicy(PyQt4.QtGui.QSizePolicy.Expanding, PyQt4.QtGui.QSizePolicy.Expanding)
        self.icon.setMinimumSize(32,32)
        self.icon.setPixmap(PyQt4.QtGui.QPixmap('./Image_Files/error.png'))
        self.iconLabel = PyQt4.QtGui.QLabel()
        self.iconLabel.setAlignment(PyQt4.QtCore.Qt.AlignRight)
        self.iconLabel.setSizePolicy(PyQt4.QtGui.QSizePolicy.Expanding, PyQt4.QtGui.QSizePolicy.Expanding)
        self.iconLabel.setMinimumSize(32,32)
        self.iconLabel.setPixmap(PyQt4.QtGui.QPixmap('./Image_Files/close2.png'))
        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.iconLabel)
        self.setLayout(self.layout)
        self.setAutoFillBackground(True)
        self.setGeometry(300,0,300,0)
        self.__revealAnimation = PyQt4.QtCore.QPropertyAnimation(self, "geometry")
        self.__revealAnimation.setDuration(250)
        self.__revealAnimation.setStartValue(PyQt4.QtCore.QRect(1300,-105,500,105))
        self.__revealAnimation.setEndValue(PyQt4.QtCore.QRect(1300,0,500,105))

        self.__hideAnimation = PyQt4.QtCore.QPropertyAnimation(self, "geometry")
        self.__hideAnimation.setDuration(100)
        self.__hideAnimation.setStartValue(PyQt4.QtCore.QRect(1300,0,500,105))
        self.__hideAnimation.setEndValue(PyQt4.QtCore.QRect(1300,-105,500,105))
        self.show()
        #self.setStyleSheet("QFrame {background : rgba(30,139,195,230)}"
        #                  "QFrame QLabel {background : rgba(30,139,195,0);padding: 10px;}")

        #self.setStyleSheet("QFrame {background : rgba(0,177,106,230)}"
        #                   "QFrame QLabel {background : rgba(30,139,195,0);padding: 10px;}")

        self.setStyleSheet("QFrame {background : rgba(207,0,15,230)}"
                          "QFrame QLabel {background : rgba(207,0,15,0);padding: 10px;}")
        self.mousePressEvent = self.hide


    def reveal(self):

        self.__revealAnimation.start()


    def hide(self, event):

        self.__hideAnimation.start()
