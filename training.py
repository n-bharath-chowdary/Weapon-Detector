import torch
from ultralytics import YOLO
import matplotlib.pyplot as plt
import os

# Define dataset path and model parameters
data_yaml = os.path.abspath(r"D:\pycharm\projects\cancer\new\projects\ashwini\security_xray.v2i.yolov5pytorch\data.yaml")  # Ensure the absolute path
print(f"Checking dataset path: {data_yaml}")  # Debugging output

EPOCHS = 8  # Number of epochs for training
BATCH = 8  # Adjust based on GPU memory

# Ensure the dataset YAML file exists
if not os.path.exists(data_yaml):
    raise FileNotFoundError(f"Dataset YAML file not found: {data_yaml}")

# Initialize YOLO model from scratch
model = YOLO("yolov5s.yaml")  # Train from scratch

# Train the model
history = model.train(data=data_yaml, epochs=EPOCHS, batch=BATCH, imgsz=320)

# Save the trained model
model_path = "best.pt"
print(f"Training complete. Model saved at {model_path}")

# Plot training history
plt.figure(figsize=(12, 5))

# Loss Plot
plt.subplot(1, 2, 1)
plt.plot(history['train/loss'], label='Train Loss')
plt.plot(history['val/loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Model Loss')
plt.legend()

# mAP (Mean Average Precision) Plot
plt.subplot(1, 2, 2)
plt.plot(history['metrics/mAP_50'], label='mAP@50')
plt.plot(history['metrics/mAP_50-95'], label='mAP@50-95')
plt.xlabel('Epochs')
plt.ylabel('mAP')
plt.title('Model mAP Performance')
plt.legend()

plt.show()
