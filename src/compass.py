from PyQt4.Qwt5 import Qwt
from PyQt4.Qwt5.Qwt import QwtCompass

class Compass(QwtCompass):
    
    def __init__(self, *args):
        QwtCompass.__init__(self, *args)
        self.rose = Qwt.QwtSimpleCompassRose(16,2)
        self.rose.setWidth(0.15)
        self.setRose(self.rose)
        self.setGeometry(600,410,140,140)
        self.show()