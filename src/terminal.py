from PyQt4.Qt import QWidget, QProcess, QVBoxLayout

class embterminal(QWidget):
    
    def __init__(self):
        QWidget.__init__(self)
        self.process = QProcess(self)
        self.terminal = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.terminal)
        self.process.start('xterm',['-into',str(self.terminal.winId())])