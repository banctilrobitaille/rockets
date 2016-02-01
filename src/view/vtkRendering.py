from PyQt4 import QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
 
class rocketRendering(QtGui.QFrame):
 
    def __init__(self, parent):
        QtGui.QFrame.__init__(self, parent)
        
        self.setGeometry(1000,620,400,400)
        self.vl = QtGui.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self)
        self.vl.addWidget(self.vtkWidget)
        self.setLayout(self.vl)
        
       # self.show()