import base64
import cv2
import numpy as np
from flask import Flask
from flask_socketio import SocketIO, emit
from ultralytics import YOLO

# 1. Initialize Server & AI
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*") 
print("Waking up YOLO...")
model = YOLO("yolov8n.pt") 
print("Brain is online.")

# 2. The Vision Logic (The Catch & Think Loop)
@socketio.on('stream_frame')
def handle_frame(data):
    try:
        # A. Catch the Image: The phone sends the image as a long string of text (Base64). 
        # We decode it back into a physical image format that OpenCV can read.
        image_data = base64.b64decode(data['image'].split(',')[1])
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # B. Think (Run YOLO): Tell the AI to look at the image.
        # Added conf=0.6 so it ONLY reports things it is 60% or more sure about
        results = model.predict(img, conf=0.6, verbose=False)

        # C. Read the Results
        detected_items = []
        for r in results:
            for box in r.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                detected_items.append(class_name)

        # D. Speak (Send Alert Back)
        if detected_items:
            unique_items = list(set(detected_items))
            alert_message = f"Detected: {', '.join(unique_items)}"
            
            # Added flush=True to force the terminal to print immediately
            print(f"AI Alert: {alert_message}", flush=True) 
            emit('audio_alert', {'message': alert_message})

    except Exception as e:
        print(f"Vision Node Error: {e}")

if __name__ == '__main__':
    print("Awaiting camera feed on port 5000...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)