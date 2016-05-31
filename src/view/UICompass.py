from PyQt4.Qwt5 import Qwt
from PyQt4.Qwt5.Qwt import QwtCompass

"""#############################################################################
# 
# Nom du module:          Compass
# Auteur:                 Benoit Anctil-Robitaille, Amine Waddah
# Date:                   8 Septembre 2015
# Description:            Le module UICompass.py regroupe les classes necessaire
#                         a laffichage dun compas. Celui ci affiche la direction
#                         (Nord-Sud-Est-Ouest)de la fusee durant le vol.
#
##############################################################################"""
from PyQt4.Qt import QPalette, QColor

"""#
# La classe Compass
# Description:    Classe representant un objet de type QwtCompass
#"""
class Compass(QwtCompass):

    def __init__(self, *args):
        QwtCompass.__init__(self, *args)
        
        
        self.needle = Qwt.QwtCompassMagnetNeedle()
        self.needlePalette = QPalette()
        self.compassPalette = QPalette()
        self.needlePalette.setColor(self.needlePalette.Light, QColor(102,0,0))
        self.needlePalette.setColor(self.needlePalette.Dark, QColor(255,255,255))
        self.compassPalette.setColor(self.compassPalette.WindowText, QColor(55,55,55))
        self.compassPalette.setColor(self.compassPalette.Text, QColor(102,0,0))
        self.needle.setPalette(self.needlePalette)
        self.setPalette(self.compassPalette)
        self.setNeedle(self.needle)
        self.setGeometry(545,350,125,125)
        self.show()
