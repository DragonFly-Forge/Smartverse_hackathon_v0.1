# Smartverse Backend: Vision Node 

This repository contains the real-time YOLOv8 object detection server and the Edge Node frontend.

##  How to Setup Your Local Environment

**1. Clone the repository**
```bash
git clone [https://github.com/DragonFly-Forge/Smartverse_hackathon_v0.1.git](https://github.com/DragonFly-Forge/Smartverse_hackathon_v0.1.git)
cd Smartverse_hackathon_v0.1
```

**2. Build your local sandbox**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install the AI and Server dependencies**
```bash
pip install -r requirements.txt
```

**4. Start the Server**
```bash
python start.py
```
*Note: The first time you run this, it will automatically download the `yolov8n.pt` weights file.*
