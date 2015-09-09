from PyQt4.Qwt5 import Qwt
from PyQt4.Qwt5.Qwt import QwtCompass

"""#############################################################################
# 
# Nom du module:          Compass
# Auteur:                 Benoit Anctil-Robitaille, Amine Waddah
# Date:                   8 Septembre 2015
# Description:            Le module compass.py regroupe les classes necessaire
#                         a laffichage dun compas. Celui ci affiche la direction
#                         (Nord-Sud-Est-Ouest)de la fusee durant le vol.
#
##############################################################################"""

"""#
# La classe Compass
# Description:    Classe representant un objet de type QwtCompass
#"""
class Compass(QwtCompass):

    def __init__(self, *args):
        QwtCompass.__init__(self, *args)
        self.rose = Qwt.QwtSimpleCompassRose(16) #Defini le nombre d'aiguille du compass
        self.rose.setWidth(0.15) #Defini la largeur des aiguilles du compass
        self.setRose(self.rose) #Initialise la rose du compass
        self.setGeometry(600,410,140,140) #Positionne le compass
        self.show() #Affiche le compass
        