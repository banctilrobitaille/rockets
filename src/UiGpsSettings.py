import PyQt4

"""#############################################################################
# 
# Nom du module:          UiGpsSettings
# Auteur:                 Benoit Anctil-Robitaille, Amine Waddah
# Date:                   8 Septembre 2015
# Description:            Le module UiGpsSetting.py regroupe les classes necessaires
#                         a laffichage de la fenetre permettant la modification des
#                         parametres de la position GPS.
#
##############################################################################"""
class GpsSettingWindow(PyQt4.QtGui.QWidget):
    
    def __init__(self,map,parent=None):
        
        PyQt4.QtGui.QWidget.__init__(self, parent)
        self.map = map
        self.__setupUi()
    
    """
    #    Methode __setupUi
    #    Description: Methode initialisant les composants graphiques
    #                 de la fenetre et les positionne.
    #
    #    param:  None
    #    return: None
    """  
    def __setupUi(self):
        
        self.setObjectName("frmGpsSetting")
        self.setFixedSize(447, 120)
        self.setWindowTitle("Base Station Position")
        
        self.gbConfig = PyQt4.QtGui.QGroupBox(self)
        self.gbConfig.setGeometry(PyQt4.QtCore.QRect(10, 10, 431, 131))
        self.gbConfig.setObjectName("gbGpsConfig")
        self.gbConfig.setTitle("Base Station Coordinate")

        self.lblLongitude = PyQt4.QtGui.QLabel(self.gbConfig)
        self.lblLongitude.setGeometry(PyQt4.QtCore.QRect(30, 20, 121, 20))
        self.lblLongitude.setObjectName("lblLongitude")
        self.lblLongitude.setText("Longitude:")
        
        self.lblLatitude = PyQt4.QtGui.QLabel(self.gbConfig)
        self.lblLatitude.setGeometry(PyQt4.QtCore.QRect(30, 50,121, 16))
        self.lblLatitude.setObjectName("lblLalitude")
        self.lblLatitude.setText("Latitude:")
        
        self.txtLongitude = PyQt4.QtGui.QLineEdit(self.gbConfig)
        self.txtLongitude.setGeometry(PyQt4.QtCore.QRect(160, 20, 100, 22))
        self.txtLongitude.setObjectName("txtLongitude")
        self.txtLongitude.setText(str(self.map.baseStation_Longitude))
        
        self.txtLatitude = PyQt4.QtGui.QLineEdit(self.gbConfig)
        self.txtLatitude.setGeometry(PyQt4.QtCore.QRect(160, 50,100, 22))
        self.txtLatitude.setObjectName("txtLatitude")
        self.txtLatitude.setText(str(self.map.baseStation_Latitude))
        
        """Initialisation et posistionnement du bouton <Cancel> """
        self.btnCancel = PyQt4.QtGui.QPushButton(self.gbConfig)
        self.btnCancel.setGeometry(PyQt4.QtCore.QRect(320, 80, 93, 28))
        self.btnCancel.setObjectName("btnCancel")
        self.btnCancel.setText("Cancel")
        
        """Initialisation et positionnement du bouton <Save>"""
        self.btnSave = PyQt4.QtGui.QPushButton(self.gbConfig)
        self.btnSave.setGeometry(PyQt4.QtCore.QRect(210, 80, 93, 28))
        self.btnSave.setObjectName("btnSave")
        self.btnSave.setText("Save")
        
        PyQt4.QtCore.QMetaObject.connectSlotsByName(self)
        self.__connectSlot()
        
    def __connectSlot(self):
        
        self.connect(self.btnCancel, PyQt4.QtCore.SIGNAL("clicked()"), self.__slotBtnCancel_Clicked)
        self.connect(self.btnSave, PyQt4.QtCore.SIGNAL("clicked()"), self.__slotBtnSave_Clicked)
    
    def __slotBtnSave_Clicked(self):
        
        self.map.baseStation_Longitude = int(self.txtLongitude.text())
        self.map.baseStation_Latitude = int(self.txtLatitude.text())
        self.map.rocket_Longitude = self.map.rocket_Longitude + 5
        self.map.rocket_Latitude = self.map.rocket_Latitude + 5
        self.map.setBaseStation()
        self.map.setRocketPosition()
        
        self.close()
    
    def __slotBtnCancel_Clicked(self):
        
        self.close()
    
