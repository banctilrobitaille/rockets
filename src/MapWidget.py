# -*- coding: utf-8 -*-


import mapnik

from PyQt4.QtCore import *
from PyQt4.QtGui import *



# QColor for name with editable value
EditableNameColor = Qt.blue

def _build_nvp(name, value = None, editable_value = False):
    n = QStandardItem(name)
    n.setFlags(n.flags() & ~(Qt.ItemIsEditable))

    if value == None:
        return n

    if type(value) == type('str'):
        v = QStandardItem(value)
    else:
        v = QStandardItem(str(value))

    if editable_value:
        n.setForeground(EditableNameColor)
    else:
        v.setFlags(v.flags() & ~(Qt.ItemIsEditable))

    return [n, v]

def _write_attr(obj, name, value):
    attr = getattr(obj, name)
    if type(attr) == type('str'):
        setattr(obj, name, value)
    elif type(attr) == type(1):
        setattr(obj, name, int(value))
    elif type(attr) == type(mapnik.Color('black')):
        setattr(obj, name, mapnik.Color(value))
    elif type(attr) == type(True):
        # '1'/'true'/'on' for True, other string for False
        setattr(obj, name, value == '1' or value.lower() == 'true' or value.lower() == 'on')



class MapnikWidget(QWidget):

    def __init__(self, also_build_view = True, parent = None):
        QWidget.__init__(self, parent)

        self.map          = mapnik.Map(256, 256)
        self.qim          = QImage()
        self.startDragPos = QPoint()
        self.endDragPos   = QPoint()
        self.zoomPos      = QPoint()
        self.drag         = False
        self.scale        = False
        self.total_scale  = 1.0

        self.timer        = QTimer()
        self.timer.timeout.connect(self.updateMap)

        self.map_tree     = QStandardItemModel()

        self.root         = _build_nvp('map')
        self.envelopeItem = _build_nvp(str(self.map.envelope()))
        self.widthItem    = _build_nvp(str(self.map.width))
        self.heightItem   = _build_nvp(str(self.map.height))
        self.layers       = _build_nvp('layers')

        if also_build_view:
            self.treeView     = QTreeView()
            self.treeView.setModel(self.map_tree)


    def buildMapTree(self):
        self.map_tree.clear()
        # recreate these data attributes, since the underlying
        # qt4 lib may already delete the actual c++ object
        # managed by map_tree on previous call.
        self.root         = _build_nvp('map')
        self.envelopeItem = _build_nvp(str(self.map.envelope()))
        self.widthItem    = _build_nvp(str(self.map.width))
        self.heightItem   = _build_nvp(str(self.map.height))
        self.layers       = _build_nvp('layers')

        self.map_tree.setHorizontalHeaderLabels(['name','value'])
        self.root.appendRow(_build_nvp('srs', self.map.srs, True))
        self.root.appendRow([_build_nvp('envelope'), self.envelopeItem])
        self.root.appendRow(_build_nvp('background', self.map.background.to_hex_string(), True))
        self.root.appendRow(_build_nvp('buffer_size', self.map.buffer_size, True))
        self.root.appendRow(_build_nvp('aspect_fix_mode', self.map.aspect_fix_mode))
        self.root.appendRow([_build_nvp('width'), self.widthItem])
        self.root.appendRow([_build_nvp('height'), self.heightItem])

        for i, layer in enumerate(self.map.layers):
            status = 'off'
            if layer.active:
                status = 'on'
            layer_item = _build_nvp(str(i)+'. ' + layer.name, status, True)
            item = layer_item[0]
            #item.appendRow(_build_nvp('name', layer.name))
            #item.appendRow(_build_nvp('active', layer.active, True))
            item.appendRow(_build_nvp('srs', layer.srs, True))
            item.appendRow(_build_nvp('maxzoom', layer.maxzoom, True))
            item.appendRow(_build_nvp('minzoom', layer.minzoom, True))
            item.appendRow(_build_nvp('clear_label_cache', layer.clear_label_cache, True))
            item.appendRow(_build_nvp('queryable', layer.queryable, True))
            item.appendRow(_build_nvp('title', layer.title))
            item.appendRow(_build_nvp('abstract', layer.abstract))

            self.layers.appendRow(layer_item)

        self.root.appendRow(self.layers)
        self.map_tree.appendRow(self.root)


    def updateMapTree(self):
        for row in range(0, self.root.rowCount()):
            name  = self.root.child(row, 0)
            value = self.root.child(row, 1)
            if name.foreground().color() == EditableNameColor: # skip non editable and non leaf item
                _write_attr(self.map, str(name.text()), str(value.text()))

        for row in range(0, self.layers.rowCount()):
            layer = self.map.layers[row]
            _write_attr(layer, 'active', str(self.layers.child(row, 1).text()))
            layer_item = self.layers.child(row)
            for srow in range(0, layer_item.rowCount()):
                name  = layer_item.child(srow, 0)
                value = layer_item.child(srow, 1)
                if name.foreground().color() == EditableNameColor: # skip non editable and non leaf item
                    _write_attr(layer, str(name.text()), str(value.text()))

        self.updateMap()

    def open(self, xml):
        # recreate a Map, or the map object will be corrupted
        self.map = mapnik.Map(self.width(), self.height())
        mapnik.load_map(self.map, xml)
        self.buildMapTree()
        self.zoom_all()

    def close_map(self):
        self.map = mapnik.Map(256, 256)
        self.updateMap()

    def updateMap(self):
        self.timer.stop()

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

        self.envelopeItem.setText(str(self.map.envelope()))
        self.widthItem.setText(str(self.map.width))
        self.heightItem.setText(str(self.map.height))

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
        painter.drawText(10, 19, 'Scale Denominator: ' + str(self.map.scale_denominator()))

    def zoom_all(self):
        self.map.zoom_all()
        self.updateMap()

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