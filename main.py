import sys
import cv2
import torch
import time
import os
import psutil
import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QHBoxLayout,
    QMenuBar,
    QMenu,
    QAction,
    QMessageBox,
)
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon
from PyQt5.QtCore import QTimer, Qt
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
to_phone_number = os.getenv('TO_PHONE_NUMBER')

twilio_client = Client(twilio_sid, twilio_auth_token)

class GuardianEye(QWidget):
    def __init__(self):
        """ 
        Initialize the GuardianEye class
        """ 
        super().__init__()
        self.initUI()
        self.model = torch.hub.load(
            "ultralytics/yolov5", "custom", path="model/guns.pt"
        )
        self.model.conf = 0.52
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)

    def initUI(self):
        """ 
        This method sets up the user interface, 
        including the layout, menu bar, labels, and buttons.
        """
        self.setWindowTitle("GuardianEye")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.menu_bar = QMenuBar(self)

        self.help_menu = QMenu("Help", self)
        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.about)
        self.help_menu.addAction(self.about_action)
        self.menu_bar.addMenu(self.help_menu)

        self.layout.setMenuBar(self.menu_bar)

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(640, 480)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.text_label = QLabel(self)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.text_label.setStyleSheet("color: red")

        self.center_layout = QHBoxLayout()
        self.center_layout.addStretch()
        self.center_layout.addWidget(self.image_label)
        self.center_layout.addStretch()

        self.layout.addLayout(self.center_layout)
        self.layout.addWidget(self.text_label)

        self.button_layout = QHBoxLayout()

        self.upload_button = QPushButton("Upload Video", self)
        self.upload_button.clicked.connect(self.uploadVideo)
        self.button_layout.addWidget(self.upload_button)

        self.start_button = QPushButton("Start Detection", self)
        self.start_button.clicked.connect(self.startDetection)
        self.button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Detection", self)
        self.stop_button.clicked.connect(self.stopDetection)
        self.button_layout.addWidget(self.stop_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

    def about(self):
        """ 
        This method displays the about dialog box.
        """
        QMessageBox.about(
            self,
            "About",
            "GuardianEye is a weapon detection application that uses YOLOv5 to detect guns in a video stream. It is developed by the csc-team.",
        )

    def uploadVideo(self):
        """ 
        This method allows the user to upload a video file.
        """
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video File",
            "",
            "Video Files (*.mp4 *.avi *.mov)",
            options=options,
        )
        if file_name:
            self.cap = cv2.VideoCapture(file_name)

    def startDetection(self):
        if self.cap is not None and self.cap.isOpened():
            self.timer.start(30)

    def stopDetection(self):
        self.timer.stop()


    def updateFrame(self):
        """ 
        This method updates the frame and displays the detected objects.
        the lines commented are used for performance evaluation
        """
        start_time = time.time()
        ret, frame = self.cap.read()
        if ret:
            results = self.model(frame)
            end_time = time.time()
            processing_time = end_time - start_time
            # print(f"Processing time: {processing_time} seconds")

            results.render()
            img_with_boxes = np.squeeze(results.render())
            img_with_boxes = cv2.cvtColor(img_with_boxes, cv2.COLOR_BGR2RGB)
            height, width, channel = img_with_boxes.shape
            bytes_per_line = 3 * width
            q_image = QImage(
                img_with_boxes.data, width, height, bytes_per_line, QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(q_image)
            pixmap_resized = pixmap.scaled(
                self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio
            )
            self.image_label.setPixmap(pixmap_resized)

            detected_classes = [results.names[int(x[-1])] for x in results.xyxy[0]]
            if "pistol" in detected_classes or "gun" in detected_classes:
                self.text_label.setText("Gun Detected!, call 911 immediately!")
                self.timer.stop()
                message = twilio_client.messages.create(
                    body="Emergency Alert: A gun has been detected. Please evacuate the premises immediately!.",
                    from_=twilio_phone_number,
                    to=to_phone_number
                )
            else:
                self.text_label.setText("No Gun Detected")
        else:
            self.cap.release()
            self.timer.stop()

        # print("CPU usage: ", psutil.cpu_percent())
        # print("Memory usage: ", psutil.virtual_memory().percent)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GuardianEye()
    ex.show()
    sys.exit(app.exec_())
