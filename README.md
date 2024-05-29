# GuardianEye - A Weapon Detection Application

## 1. Introduction
GuardianEye is a sophisticated computer vision application designed to detect weapons, particularly guns, in video streams. This report provides an in-depth analysis of the project's theoretical foundations, development methodologies, implementation details, and performance evaluation.

## 2. Theoretical Foundations

### 2.1 Computer Vision
Computer vision, a branch of artificial intelligence, empowers machines to interpret and comprehend the visual world. By analyzing digital images and videos, computer vision systems can accurately identify and classify objects.

### 2.2 Object Detection
Object detection involves identifying and locating objects within images or videos. Traditional methods such as Haar Cascades and modern deep learning-based approaches like YOLO (You Only Look Once) are commonly used for this task.

### 2.3 YOLO Algorithm
YOLO is a state-of-the-art, real-time object detection system that treats object detection as a single regression problem. By predicting bounding box coordinates and class probabilities directly from image pixels, YOLO achieves high accuracy and processing speed.

## 3. Development Methodologies

### 3.1 Agile Development
The project embraced Agile methodologies to foster iterative progress, ensuring continuous feedback loops and adaptability to evolving requirements.

### 3.2 Data Collection and Preprocessing
A diverse dataset containing annotated images of weapons was collected from various sources. Data augmentation techniques were applied to enhance dataset diversity and size.

### 3.3 Model Training
The YOLOv5s model was selected. Training was conducted on Google Colab utilizing it's free GPU resources for faster computation.

## 4. Implementation Details

### 4.1 Software Architecture
The application was developed using Python and integrated with PyQt5 for the graphical user interface. YOLOv5 served as the real-time weapon detection model.

### 4.2 Core Components
- **Model Integration:** YOLOv5 model was seamlessly integrated using the `torch.hub` module.
- **Video Processing:** OpenCV facilitated video capture and frame processing.
- **GUI Development:** PyQt5 provided robust tools for designing the user interface.

### 4.3 User Interface
The user interface featured functionalities for uploading video files, initiating and halting detection, and displaying real-time results.

## 5. Performance Evaluation

### 5.1 Accuracy and Detection Rate
Model accuracy and detection rate were evaluated using a comprehensive test set. Metrics like precision, recall, and F1-score were computed to assess performance.

### 5.2 Computational Performance
Performance analysis was conducted on CPU configuration only. Limitations imposed by the absence of CUDA-capable hardware impacts real-time processing capabilities.

### 5.3 Key Findings
- **False Positives:** Occasional false positives were observed due to the limited dataset and varying video angles.
- **Hardware Constraints:** The absence of CUDA-enabled devices hampered video processing performance, highlighting the need for improved hardware infrastructure.
- **Quality:** The quality of the video significantly impacts the accuracy of the detection process. It has been observed that videos with lower resolution tend to produce more false positives. Here are some common resolutions and their impact:

    - **480p (SD): 854x480** - This resolution provides a balance between quality and performance. However, it may still produce some false positives.

    - **360p (SD): 640x360** - At this resolution, the accuracy of detection decreases, leading to a higher number of false positives.

    - **240p (SD): 426x240** - This is the lowest resolution tested, and it resulted in the highest number of false positives. It is not recommended for accurate detection.

## 6. Challenges and Limitations

### 6.1 Dataset Limitations
The project encountered challenges related to the limited dataset, leading to occasional false positives. Expanding the dataset and incorporating diverse scenarios is essential for improving model accuracy.

### 6.2 Hardware Limitations
The absence of CUDA-enabled hardware posed significant limitations on processing speed and efficiency. Future endeavors should prioritize hardware upgrades to enhance real-time detection capabilities.

## 7. Future Work

### 7.1 Dataset Expansion
Enhancing the dataset by including additional classes like assault rifles, submachine guns, and shotguns will improve model robustness and accuracy.

### 7.2 Hardware Upgrades
Leveraging CUDA-capable devices and exploring hardware acceleration techniques like OpenCL will enhance processing speed and efficiency.

### 7.3 Integrating Additional Sensors
Combining visual data with other sensor inputs will augment detection accuracy and reliability, facilitating the development of comprehensive surveillance systems.

## 8. Conclusion
GuardianEye represents a significant advancement in computer vision applications for public safety. Despite challenges, the project lays the foundation for future enhancements in accuracy, performance, and real-world deployment.

