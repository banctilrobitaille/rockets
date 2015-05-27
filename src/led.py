from PyKDE4.kdeui import KLed
from PyQt4 import QtGui


class Led(KLed):
    
    def init(self):
        #self.peakLED = KLed(self)
        self.setColor(QtGui.QColor(400,200,300))
        self.setGeometry(350,200,300,300)
        self.show()