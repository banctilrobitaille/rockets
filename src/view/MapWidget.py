# -*- coding: utf-8 -*-
import mapnik
import simplekml
import PyQt4


class MapnikWidget(PyQt4.QtGui.QWidget):

    def __init__(self,parent, also_build_view = True):
        
        PyQt4.QtGui.QWidget.__init__(self, parent)
        
        self.baseStation_Latitude = 0
        self.baseStation_Longitude = 0
        self.rocket_Latitude = 0
        self.rocket_Longitude = 0
        
        self.map = mapnik.Map(15000, 15000, "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs")
        self.basekml = simplekml.Kml()
        self.rocketkml = simplekml.Kml()
        self.baseStationPoint = self.basekml.newpoint(name="BaseStation")
        self.rocketPoint = self.rocketkml.newpoint(name="Rocket")
        
        self.qim          = PyQt4.QtGui.QImage()
        self.startDragPos = PyQt4.QtCore.QPoint()
        self.endDragPos   = PyQt4.QtCore.QPoint()
        self.zoomPos      = PyQt4.QtCore.QPoint()
        self.drag         = False
        self.scale        = False
        self.total_scale  = 1.0
        self.map.zoom_all()
        
        self.timer        = PyQt4.QtCore.QTimer()
        self.timer.timeout.connect(self.updateMap)

        self.map_tree     = PyQt4.QtGui.QStandardItemModel()
        
        
    def open(self, xml):
        
        self.map = mapnik.Map(self.width(), self.height())
        mapnik.load_map(self.map, xml)
        self.map.resize(900,600)
        self.map.zoom(145.0)
        self.updateMap()
        #self.map.zoom_all()
        
    def setBaseStation(self):
        
        #self.kml.newpoint(name="BaseStation", coords=[(self.baseStation_Longitude,self.baseStation_Latitude)])
        try:
            del self.map.layers[1]
        except:
            pass
        self.baseStationPoint.coords = [(self.baseStation_Longitude, self.baseStation_Latitude)]
        self.basekml.save("GPS_BaseStation.kml")
        style = mapnik.Style()
        rule = mapnik.Rule()
        point_symbolizer = mapnik.MarkersSymbolizer()
        point_symbolizer.filename = "home.svg"
        point_symbolizer.transform = "scale(1)"
        point_symbolizer.allow_overlap = False
        point_symbolizer.opacity = 1
        rule.symbols.append(point_symbolizer)
        style.rules.append(rule)
        self.map.append_style("GPS_BaseStation", style)
        self.baselayer = mapnik.Layer("GPS_BaseStation")
        self.baselayer.datasource = mapnik.Ogr(file="GPS_BaseStation.kml", layer_by_index=0)
        self.baselayer.styles.append("GPS_BaseStation")
        self.map.layers.append(self.baselayer)
        self.updateMap()

        
    def setRocketPosition(self):
        
        try:
            del self.map.layers[2]
        except:
            pass
        
        self.rocketPoint.coords = [(self.rocket_Longitude, self.rocket_Latitude)]
        self.rocketkml.save("GPS_Rocket.kml")
        style = mapnik.Style()
        rule = mapnik.Rule()
        point_symbolizer = mapnik.MarkersSymbolizer()
        point_symbolizer.filename = "rocket.svg"
        point_symbolizer.transform = "scale(0.2)"
        point_symbolizer.allow_overlap = False
        point_symbolizer.opacity = 1
        rule.symbols.append(point_symbolizer)
        style.rules.append(rule)
        self.map.append_style("GPS_Rocket", style)
        self.rocketlayer = mapnik.Layer("GPS_Rocket")
        self.rocketlayer.datasource = mapnik.Ogr(file="GPS_Rocket.kml", layer_by_index=0)
        self.rocketlayer.styles.append("GPS_Rocket")
        self.map.layers.append(self.rocketlayer)
        self.updateMap()
        
    def updateMap(self):
       
        if self.drag:
            cx = int(0.5 * self.map.width)
            cy = int(0.5 * self.map.height)
            dpos = self.endDragPos - self.startDragPos
            self.map.pan(cx - dpos.x() ,cy - dpos.y())
            self.drag = False
        elif self.scale:
            
            # scale upon the mouse cursor position
            # build up the transformation matrix
            ma = PyQt4.QtGui.QMatrix()
            # firstly, translate the cursor position to the origin
            ma.translate(self.zoomPos.x(), self.zoomPos.y())
            # then, do the normal scale upon origin
            ma.scale(self.total_scale, self.total_scale)
            # finnaly, translate back to the cursor position
            ma.translate(-self.zoomPos.x(), -self.zoomPos.y())

            rect = ma.mapRect(PyQt4.QtCore.QRectF(0, 0, self.map.width, self.map.height))
            env = mapnik.Envelope(rect.left(), rect.bottom(), rect.right(), rect.top())
            self.map.zoom_to_box(self.map.view_transform().backward(env))

            self.total_scale = 1.0
            self.scale       = False

        im = mapnik.Image(self.map.width, self.map.height)
        mapnik.render(self.map, im)
        self.qim.loadFromData(PyQt4.QtCore.QByteArray(im.tostring('png')))
        self.update()


    def paintEvent(self, event):
        painter = PyQt4.QtGui.QPainter(self)

        if self.drag:
            painter.drawImage(self.endDragPos - self.startDragPos, self.qim)
        elif self.scale:
            painter.save()
            scale = 1 / self.total_scale
            painter.translate(self.zoomPos.x(), self.zoomPos.y())
            painter.scale(scale, scale)
            painter.translate(-self.zoomPos.x(), -self.zoomPos.y())
            exposed = painter.matrix().inverted()[0].mapRect(self.rect()).adjusted(-1, -1, 1, 1)
            painter.drawImage(exposed, self.qim, exposed)
            painter.restore()
        else:
            painter.drawImage(0, 0, self.qim)

        painter.setPen(PyQt4.QtGui.QColor(0, 0, 0, 100))
        painter.setBrush(PyQt4.QtGui.QColor(0, 0, 0, 100))
        painter.drawRect(0, 0, 256, 26)
        painter.setPen(PyQt4.QtGui.QColor(0, 255 , 0))
        painter.drawText(10, 19, 'Rockets Position')


    def wheelEvent(self, event):
        self.zoomPos     = event.pos()
        self.total_scale *= 1.0 - event.delta() / (360.0 * 8.0) * 4
        self.scale = True

        self.update()
        self.timer.start(400)


    def mousePressEvent(self, event):
        if event.button() == PyQt4.QtCore.Qt.LeftButton:
            self.startDragPos = event.pos()
            self.drag         = True

    def mouseMoveEvent(self, event):
        if self.drag:
            self.endDragPos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == PyQt4.QtCore.Qt.LeftButton:
            self.endDragPos = event.pos()
            self.updateMap()