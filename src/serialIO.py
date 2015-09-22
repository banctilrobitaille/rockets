import serial
import PyQt4

"""#############################################################################
# 
# Nom du module:          serialIO
# Auteur:                 Benoit Anctil-Robitaille, Amine Waddah
# Date:                   8 Septembre 2015
# Description:            Le module serialIO.py regroupe les classes necessaires
#                         a louverture dune connexion serie, lecture de donnees 
#                         recues sur la connexion serie et traitement des donnees
#
##############################################################################"""

"""#
# La classe SerialConnection
# Description:    Classe representant une connexion serie
#"""
class SerialConnection(serial.Serial):
    
    
    trigger = PyQt4.QtCore.pyqtSignal(int,int,int)
    
    def __init__(self):
        
        serial.Serial.__init__(self)
        self.port = "/dev/ttyS0"
        
        """Initialisation des parametres relatifs au port serie
        compatible avec le RFD900"""
        
        """Initialisation du baudrate  a 57600"""
        self.baudrate = 57600
        """Utilisation de 1 bit darret"""
        self.stopbits = serial.STOPBITS_ONE
        """Aucune parite"""
        self.parity = serial.PARITY_NONE
        """8 bits/trame"""
        self.bytesize = serial.EIGHTBITS
        self.isConnected = False
        self.i = 0
        self.j = 0
        self.k = 0
    
    """
    #    Methode handleData
    #    Description: Methode qui decortique les trames de donnees recues
    #                 et qui emet un signal lors de la reception de donnees
    #
    #    param: data: Les donnees recues par la station
    #           
    #            
    #    return: None
    """   
    def handleData(self, data):
        
        """Signal la reception de donnees. Le signal est 
        traite par le GUI pour mettre a jour laffichage"""
        self.trigger.emit(self.i, self.j, self.k)
        data.encode()
        
    """
    #    Methode readFromSerialPort
    #    Description: Methode qui lit les donnees sur le port serie et qui appel
    #                 la methode handleData afin de les decortiquer
    #                 
    #
    #    param: 
    #           
    #            
    #    return: None
    """   
    def readFromSerialPort(self):
        
        """Lecture des donnees en attente dans le buffer serie"""
        data = self.read(self.inWaiting())
        """Decortication des donnees"""
        self.handleData(data)
        

"""#
# La classe thread
# Description:    Classe representant un thread
#"""        
class Thread(PyQt4.QtCore.QThread):
    
    """Sends signal when connected to update the GUI"""
    isconnected = PyQt4.QtCore.pyqtSignal(bool)
    """Sends signal when data is received to update the GUI"""
    receivedata = PyQt4.QtCore.pyqtSignal(int, int, int)
    
    """
    #    Constructeur
    #    Description: Constructeur de la classe Thread
    #
    #    param: serialConnection: La connexion serie de lapplication
    #
    #    return: None
    """
    def __init__(self, serialConnection):
        self.serialConnection = serialConnection
        PyQt4.QtCore.QThread.__init__(self)
        """Le thread nest pas demarrer par defaut"""
        self.isRunning = False
    
    """
    #    Methode startCommunication
    #    Description: Methode qui initie la communication serie et qui 
    #                 signal letat de la connexion
    #
    #    param:
    #           
    #            
    #    return: None
    """   
    def startCommunication(self):
        
        try:
            """Ouverture de la connexion"""
            self.serialConnection.open()
            """Mise a jour de letat de la connexion"""
            self.serialConnection.isConnected = True
            """Mise a jour de letat du thread"""
            self.isRunning = True
            """Demarrage du thread"""
            self.start()
            """Signalement de letat de la connexion"""
            self.isconnected.emit(self.serialConnection.isConnected)
        except serial.serialutil.SerialException:
            """Affichage en cas derreur lors de louverture de la connexion serie"""
            PyQt4.QtGui.QMessageBox.about(PyQt4.QtGui.QWidget(), "Error", "Unable to open the com port: " + str(self.serialConnection.port))
     
     
    """
    #    Methode stopCommunication
    #    Description: Methode qui coupe la communication serie et qui en avise
    #                 le GUI a laide dun signal
    #
    #    param:
    #           
    #            
    #    return: None
    """           
    def stopCommunication(self):
        
        """Si une communication est active on la stop"""
        if self.serialConnection.isConnected:
            
            try: 
                
                """Mise a jour de letat du thread"""
                self.isRunning = False
                """Fermeture de la connexion serie"""
                self.serialConnection.close()
                """Mise a jour de letat de la connexion serie"""
                self.serialConnection.isConnected = False
                """Signalement dun changement detat de la connexion"""
                self.isconnected.emit(self.serialConnection.isConnected)
            except serial.serialutil.SerialException:
                
                """Affichage dun message derreur si erreur lors de la fermeture de la connexion"""
                PyQt4.QtGui.QMessageBox.about(PyQt4.QtGui.QWidget(), "Error", "Unable to close the com port: " + str(self.serialConnection.port))
        
        else:
            
            """Affichage si aucune connexion est ouverte"""
            PyQt4.QtGui.QMessageBox.about(PyQt4.QtGui.QWidget(), "Oups", "No connection currently opened !")
            
    """
    #    Methode run
    #    Description: Methode qui est appelee lors du demarrage du thread
    #
    #    param:
    #           
    #            
    #    return: None
    """ 
    def run(self):
        
        """Tant que le thread est en vie"""
        while self.isRunning == True: 
            
            """Sil y a des donnees dans le buffer serie"""
            if self.serialConnection.inWaiting() > 0:
                
                """Lecture des donnees dans le buffer"""
                self.analysedData = self.serialConnection.readFromSerialPort()
                #self.receivedata.emit(self.analysedData[0], self.analysedData[1], self.analysedData[2])
                
            