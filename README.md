# Autonomous Driving System

## 📌 Introduction

Autonomous vehicles, also known as self-driving cars, leverage a combination of **sensors**, **cameras**, **radar**, and **artificial intelligence** to navigate and drive without human input. These systems are designed to:

- Reduce accidents caused by human error  
- Improve overall traffic flow  
- Provide mobility for individuals unable to drive  

Companies such as **Waymo**, **Tesla**, and **Cruise** are pioneers in this space, conducting large-scale testing on public roads. Despite substantial advancements, widespread deployment still faces hurdles including:

- Safety regulations  
- Public trust and acceptance  
- Technological and environmental limitations  

---

## ❓ Problem Statement & Vision

This project aims to develop an **AI-driven autonomous driving system** capable of **real-time decision-making**, prioritizing **safety** and **efficiency**. It focuses on navigating dynamic environments and managing uncertainties using a modular AI architecture.

---

## 🔧 Core Algorithms & Technologies

### 📍 Route Planning
**Dijkstra’s Algorithm**  
Used for calculating optimal routes by incorporating:
- Real-time traffic updates  
- Dynamic road conditions  
- Adaptive pathfinding logic  

### ⚠️ Risk Assessment
**Bayesian Networks**  
Models probabilistic relationships to assess risks related to:
- Weather conditions  
- Pedestrian behavior  
- Sensor reliability  

Ensures robust decision-making under uncertainty.

### 👁️ Object Detection (Perception Module)
**Deep Learning (CNNs, YOLO, Faster R-CNN, U-Net, ERFNet)** enables real-time object recognition and scene understanding:
- **Lane Detection**: U-Net / ERFNet for identifying lane markings under varied conditions  
- **Traffic Light Recognition**: Deep learning pipeline for detecting and classifying light colors (red, yellow, green)  
- **Stop Sign Detection**: YOLO / Faster R-CNN for accurate sign localization and classification  

### 🗣️ Driver Interaction
**Natural Language Processing (NLP)**  
Facilitates user interaction via:
- **Speech-to-text** processing  
- **Intent recognition** for setting destinations and receiving system updates  

### 🚗 Vehicle Control System
**IoT and Robotics Integration**  
Manages vehicle control through:
- Precision actuation (steering, acceleration, braking)  
- Real-time feedback from environmental sensors  
- IoT device synchronization for dynamic adjustment  

---

## 📦 Features Summary

- ✅ Real-time path planning with adaptive routing  
- ✅ Risk modeling for uncertain environments  
- ✅ Advanced object detection (lanes, signs, lights)  
- ✅ Voice-enabled driver interface  
- ✅ Sensor-integrated vehicle control system  

---
## 🚀 Getting Started: Setup & Execution Commands

To set up and run this project, execute the following commands in your terminal:

```sh
# 1. Create and activate a new conda environment
conda create --name selfdrive python=3.11
conda activate selfdrive

# 2. Install required Python packages
pip install -r requirements.txt

# 3. (Optional) Create the utils directory if it doesn't exist
mkdir utils

# 4. Launch the Streamlit application
streamlit run Home.py

# 5. When finished, deactivate the environment
conda deactivate
```

> **Note:**  
> Make sure you have [Anaconda](https://www.anaconda.com/products/distribution) and [Streamlit](https://streamlit.io/) installed on your system.


## 📚 Future Work

- Expand to multi-agent traffic simulation  
- Integrate LiDAR-based mapping  
- Enhance NLP with multilingual support  
- Explore V2V (Vehicle-to-Vehicle) communication

## Dataset Used

- Waymo : http://dl.yf.io/bdd-data/v1/videos/
- Self drive Kaggle : https://www.kaggle.com/datasets/alincijov/self-driving-cars
- Routing : https://osmnx.readthedocs.io/en/stable/
- Traffic Signal: https://www.cvlibs.net/datasets/kitti/
- Object detection: https://cocodataset.org/#download

## References

1. Celi, H. (n.d.). mission_planning.ipynb. GitHub. Retrieved from https://github.com/hankeceli/self-driving-cars/blob/master/mission_planning.ipynb
2. Cijov, A. (n.d.). Self-driving cars. Kaggle. Retrieved from https://www.kaggle.com/datasets/alincijov/self-driving-cars?resource=download
3. Furda, A., & Vlacic, L. (2010). Real-time decision making for autonomous city vehicles. Journal of Robotics and Mechatronics, 22(6), 694. https://doi.org/10.20965/jrm.2010.p0694
4. Jain, R., & Kumar, R. (2017). Autonomous driving system with real-time decision making. In 2017 International Conference on Intelligent Systems and Control (ISSC) (pp. 1-6). IEEE. https://doi.org/10.1109/ISSC.2017.8122757
5. Tendulkar, S. (2024, October). Real-time decision-making in autonomous systems: Leveraging cloud-based reinforcement learning for generative AI and adaptive resource allocation. University of Computer Studies Mandalay. https://doi.org/10.13140/RG.2.2.21323.60964
6. National Highway Traffic Safety Administration. (2023). Automated Vehicles for Safety. https://www.nhtsa.gov/technology-innovation/automated-vehicles-safety
7. Boeing, G. (2025). Modeling and Analyzing Urban Networks and Amenities with OSMnx. Geographical Analysis, published online ahead of print. doi:10.1111/gean.70009
