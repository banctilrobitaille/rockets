import PyQt4
import subprocess
from PyQt4.Qt import QString
        
class embTerminal(PyQt4.QtGui.QFrame):
    
    def __init__(self):
        
        PyQt4.QtGui.QFrame.__init__(self)
        self.setGeometry(250,250,600,600)
        self.gridLayout = PyQt4.QtGui.QGridLayout()
        
        self.terminal = PyQt4.QtGui.QTextBrowser()
        self.commandInput = PyQt4.QtGui.QLineEdit()
        self.sendButton = PyQt4.QtGui.QPushButton("Send Command")
        
        self.addWidget(self.terminal, 0, 0, 1, 2)
        self.addWidget(self.commandInput, 0, 1, 1, 1)
        self.addWidget(self.sendButton, 1, 1, 1, 1)
        self.show()
    
    def addWidget(self,widget, xGridPosition, yGridPosition, rowSpan, columnSpan):
        
        self.gridLayout.addWidget(widget, yGridPosition, xGridPosition, rowSpan, columnSpan)
        self.setLayout(self.gridLayout)
    
    def keyPressEvent(self, e):
        
        if e.key() == PyQt4.QtCore.Qt.Key_Return:
            
            if self.commandInput.text() != "":
                
                self.sendCommand(self.commandInput.text())
    
    def sendCommand(self,command):
        
        self.terminal.append(command)
        self.commandInput.clear()
