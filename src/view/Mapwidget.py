from mpl_toolkits.basemap import Basemap
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import PyQt4

class Map(PyQt4.QtGui.QWidget):

    def __init__(self, parent):

        super(Map, self).__init__(parent)

        #self.params = SubplotParams(left=0.10,wspace=0, hspace=0)
        self.fig = Figure(figsize=(12,12),frameon=False, tight_layout=False)
        self.axes = self.fig.add_axes([0,0,1,1])

        grid = np.random.rand(10, 10)
        self.canvas = FigureCanvas(self.fig)

        self.layout = PyQt4.QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.canvas)

        self.m = Basemap(width=6000000,height=4500000,projection='lcc',
            resolution='i',lat_1=45.,lat_2=55,lat_0=38.88,lon_0=-110,ax=self.axes)

        #m.drawlsmask(land_color='coral',ocean_color='aqua',lakes=True)

        self.m.bluemarble()
        self.m.drawcountries()
        self.m.drawstates()
        parallels = np.arange(0.,41,10.)
        # labels = [left,right,top,bottom]
        self.m.drawparallels(parallels,labels=[False,True,True,False], linewidth=1,color='R', textcolor='R', fontsize=9)
        meridians = np.arange(10.,351.,20.)
        self.m.drawmeridians(meridians,labels=[True,False,False,True], linewidth=1,color='R',textcolor='R', fontsize=9)
        self.lon = -110
        self.lat = 38.88

        x,y = self.m(self.lon,self.lat)
        self.marker = self.m.plot(x,y, marker="D", markersize=10, color='r')

        self.axes.imshow(grid,interpolation="quadric", aspect='auto')
        self.canvas.draw()
        self.show()

    def updateMarker(self, lon, lat):

        x,y = self.m(lon,lat)
        self.marker[0].remove()
        self.marker = self.m.plot(x,y, marker="D", markersize=10, color='r')
        self.canvas.draw()
