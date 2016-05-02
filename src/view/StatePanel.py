import PyQt4
from PyKDE4.kdeui import KLed
from model.Rocket import Rocket
'''
Created on 2016-01-31

@author: rockets
'''
from PyQt4.Qt import QColor, QFont

class StatePanel(PyQt4.QtGui.QFrame):

    def __init__(self, parent):

        super(PyQt4.QtGui.QFrame,self).__init__(parent)
        self.setGeometry(1250,530, 250,300)
        self.palette = PyQt4.Qt.QPalette()
        self.palette.setColor(self.palette.WindowText, QColor(245,245,245))
        self.gridLayout = PyQt4.QtGui.QGridLayout()
        self.__addStateToPanel()
        self.setLayout(self.gridLayout)
        self.show()
    
    def __addStateToPanel(self):
        
        for state,value in Rocket.STATE.items():
            
            led = KLed()
            
            led.setColor(QColor(255,0,0))

            iconLabel = PyQt4.QtGui.QLabel()
            iconLabel.setAlignment(PyQt4.QtCore.Qt.AlignCenter)
            iconLabel.setSizePolicy(PyQt4.QtGui.QSizePolicy.Expanding, PyQt4.QtGui.QSizePolicy.Expanding)
            iconLabel.setMinimumSize(32,32)
            iconLabel.setPixmap(PyQt4.QtGui.QPixmap('./Image_Files/running.png'))

            label = PyQt4.QtGui.QLabel(state)
            label.fontChange(QFont("Arial",20))
            label.setPalette(self.palette)
            self.gridLayout.addWidget(iconLabel,value,0)
            self.gridLayout.addWidget(label,value,1)