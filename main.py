import sys
import cv2
import torch
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QHBoxLayout, QMenuBar, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import QTimer, Qt

class WeaponDetectionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='model/guns.pt')
        self.model.conf = 0.48
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        
    def initUI(self):
        self.setWindowTitle('Weapon Detection App')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.menu_bar = QMenuBar(self)
        
        self.help_menu = QMenu('Help', self)
        self.about_action = QAction('About', self)
        self.about_action.triggered.connect(self.about)
        self.help_menu.addAction(self.about_action)
        self.menu_bar.addMenu(self.help_menu)
        
        self.layout.setMenuBar(self.menu_bar)

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(640, 480)
        self.image_label.setAlignment(Qt.AlignCenter)
        
        self.text_label = QLabel(self) 
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setFont(QFont('Arial', 20, QFont.Bold))
        self.text_label.setStyleSheet("color: red")

        self.center_layout = QHBoxLayout()
        self.center_layout.addStretch()
        self.center_layout.addWidget(self.image_label)
        self.center_layout.addStretch()

        self.layout.addLayout(self.center_layout)
        self.layout.addWidget(self.text_label)

        self.button_layout = QHBoxLayout()

        self.upload_button = QPushButton('Upload Video', self)
        self.upload_button.clicked.connect(self.uploadVideo)
        self.button_layout.addWidget(self.upload_button)

        self.start_button = QPushButton('Start Detection', self)
        self.start_button.clicked.connect(self.startDetection)
        self.button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Stop Detection', self)
        self.stop_button.clicked.connect(self.stopDetection)
        self.button_layout.addWidget(self.stop_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)
    
    def about(self):
        QMessageBox.about(self, "About", "Created with ❤️ by Allen")
    
    def uploadVideo(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mov)", options=options)
        if file_name:
            self.cap = cv2.VideoCapture(file_name)
    
    def startDetection(self):
        if self.cap is not None and self.cap.isOpened():
            self.timer.start(30)
    
    def stopDetection(self):
        self.timer.stop()
    
    def updateFrame(self):
        ret, frame = self.cap.read()
        if ret:
            results = self.model(frame)
            results.render()
            img_with_boxes = np.squeeze(results.render())
            img_with_boxes = cv2.cvtColor(img_with_boxes, cv2.COLOR_BGR2RGB)
            height, width, channel = img_with_boxes.shape
            bytes_per_line = 3 * width
            q_image = QImage(img_with_boxes.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            pixmap_resized = pixmap.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap_resized)
            
            detected_classes = [results.names[int(x[-1])] for x in results.xyxy[0]]
            if 'pistol' in detected_classes or 'gun' in detected_classes:
                self.text_label.setText('Gun Detected!, Call 911 Immediately!')
            else:
                self.text_label.setText('No Gun Detected')
        else:
            self.cap.release()
            self.timer.stop()
            self.text_label.setText('')

if __name__ == '__main__':  
    app = QApplication(sys.argv)
    ex = WeaponDetectionApp()
    ex.show()
    sys.exit(app.exec_())
