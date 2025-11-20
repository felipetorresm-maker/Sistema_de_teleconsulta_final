from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from av_call import av_client

class NewWindow(QMainWindow):
    def __init__(self,ip):
        super().__init__()
        self.resize(640,480)
        self.setWindowTitle("New Window")

        self.display_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.display_width, self.display_height)

        
        layout=QGridLayout()

        layout.addWidget(self.image_label, 0, 0, 2, 2)
        
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
    
    
    
        call=av_client(ip, self.image_label, self.display_width, self.display_height)
        print('Conectando a médico en IP:', ip)
        call.connect()
