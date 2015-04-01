# -*- coding: utf-8 -*-


import mapnik
import simplekml

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MapnikWidget(QWidget):

    def __init__(self,parent, also_build_view = True):
        QWidget.__init__(self, parent)
        
        self.kml = simplekml.Kml()
        self.kml.newpoint(name="Quebec", coords=[(-74.0, 48.0)])
        self.kml.save("GPS_tracking_data.kml")
        self.map = mapnik.Map(15000, 15000, "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext +no_defs")
        self.style = mapnik.Style()
        self.rule = mapnik.Rule()
        self.point_symbolizer = mapnik.MarkersSymbolizer()
        self.point_symbolizer.allow_overlap = True
        self.point_symbolizer.opacity = 1
        self.rule.symbols.append(self.point_symbolizer)
        self.style.rules.append(self.rule)
        self.map.append_style("GPS_tracking_points", self.style)
        self.qim          = QImage()
        self.startDragPos = QPoint()
        self.endDragPos   = QPoint()
        self.zoomPos      = QPoint()
        self.drag         = False
        self.scale        = False
        self.total_scale  = 1.0
        
        self.layer = mapnik.Layer("GPS_tracking_points")
        self.layer.datasource = mapnik.Ogr(file="GPS_tracking_data.kml", layer_by_index=0)
        self.layer.styles.append("GPS_tracking_points")
        self.map.layers.append(self.layer)
        self.map.zoom_all()
        
        self.timer        = QTimer()
        self.timer.timeout.connect(self.updateMap)

        self.map_tree     = QStandardItemModel()
        
  

    def open(self, xml):
        self.map = mapnik.Map(self.width(), self.height())
        mapnik.load_map(self.map, xml)
        self.kml = simplekml.Kml()
        self.kml.newpoint(name="Quebec", coords=[(-71.25, 46.8)])
        self.kml.save("GPS_tracking_data.kml")
        self.style = mapnik.Style()
        self.rule = mapnik.Rule()
        self.point_symbolizer = mapnik.MarkersSymbolizer()
        self.point_symbolizer.allow_overlap = False
        self.point_symbolizer.opacity = 1
        self.rule.symbols.append(self.point_symbolizer)
        self.style.rules.append(self.rule)
        self.map.append_style("GPS_tracking_points", self.style)
        self.qim          = QImage()
        self.startDragPos = QPoint()
        self.endDragPos   = QPoint()
        self.zoomPos      = QPoint()
        self.drag         = False
        self.scale        = False
        self.total_scale  = 1.0
        
        self.layer = mapnik.Layer("GPS_tracking_points")
        self.layer.datasource = mapnik.Ogr(file="GPS_tracking_data.kml", layer_by_index=0)
        self.layer.styles.append("GPS_tracking_points")
        self.map.layers.append(self.layer)
       # self.map.zoom_all()
        
        self.map.zoom(150.0)
        #self.buildMapTree()
        #self.zoom_all()

    def updateMap(self):
       # self.timer.stop()

        if self.drag:
            cx = int(0.5 * self.map.width)
            cy = int(0.5 * self.map.height)
            dpos = self.endDragPos - self.startDragPos
            self.map.pan(cx - dpos.x() ,cy - dpos.y())
            self.drag = False
        elif self.scale:
            # scale upon the mouse cursor position
            # build up the transformation matrix
            ma = QMatrix()
            # firstly, translate the cursor position to the origin
            ma.translate(self.zoomPos.x(), self.zoomPos.y())
            # then, do the normal scale upon origin
            ma.scale(self.total_scale, self.total_scale)
            # finnaly, translate back to the cursor position
            ma.translate(-self.zoomPos.x(), -self.zoomPos.y())

            rect = ma.mapRect(QRectF(0, 0, self.map.width, self.map.height))
            env = mapnik.Envelope(rect.left(), rect.bottom(), rect.right(), rect.top())
            self.map.zoom_to_box(self.map.view_transform().backward(env))

            self.total_scale = 1.0
            self.scale       = False

        im = mapnik.Image(self.map.width, self.map.height)
        mapnik.render(self.map, im)
        self.qim.loadFromData(QByteArray(im.tostring('png')))
        self.update()


    def paintEvent(self, event):
        painter = QPainter(self)

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

        painter.setPen(QColor(0, 0, 0, 100))
        painter.setBrush(QColor(0, 0, 0, 100))
        painter.drawRect(0, 0, 256, 26)
        painter.setPen(QColor(0, 255 , 0))
        painter.drawText(10, 19, 'Rockets Position')


    def resizeEvent(self, event):
        self.map.resize(event.size().width(), event.size().height())
        self.updateMap()

    def wheelEvent(self, event):
        self.zoomPos     = event.pos()
        self.total_scale *= 1.0 - event.delta() / (360.0 * 8.0) * 4
        self.scale = True

        self.update()
        self.timer.start(400)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startDragPos = event.pos()
            self.drag         = True

    def mouseMoveEvent(self, event):
        if self.drag:
            self.endDragPos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.endDragPos = event.pos()
            self.updateMap()