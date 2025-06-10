import cv2
import torch
import tkinter as tk
from tkinter import filedialog
from ultralytics import YOLO
import matplotlib.pyplot as plt

# Load trained model
model_path = 'runs/detect/train/weights/best.pt'  # Adjust the path if needed
model = YOLO(model_path)

root = tk.Tk()
root.withdraw()  # Hide root window
root.attributes('-topmost', True)  # Keep file dialog on top
image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
root.destroy()  # Destroy root window after selection

# If no file is selected, exit
if not image_path:
    print("No image selected. Exiting...")
    exit()

# Load selected image
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB for Matplotlib

# Run inference
results = model(image, conf=0.05, save=True)

# Check if any detections were made
detected = False

# Process results
for result in results:
    # print(model.names)
    if result.boxes is not None:

        boxes = result.boxes
        # print(results[0])
        for i in range(len(boxes)):
            detected = True  # At least one weapon was detected
            x1, y1, x2, y2 = map(int, boxes.xyxy[i])
            confidence = boxes.conf[i].item()
            class_id = int(boxes.cls[i])
            label = f"{model.names[class_id]}: {confidence:.2f}"

            # Draw bounding box and label
            cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image_rgb, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Apply edge detection to highlight detected regions
            roi = image[y1:y2, x1:x2]
            edges = cv2.Canny(roi, 100, 200)
            image_rgb[y1:y2, x1:x2] = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)

# Plot the image with Matplotlib
plt.figure(figsize=(8, 6))
plt.imshow(image_rgb)
plt.axis('off')  # Hide axis

# Display message on the plot
message = "Weapon Detected" if detected else "No Weapon Detected"
color = "red" if detected else "green"
plt.text(10, 30, message, fontsize=14, fontweight='bold', color=color, bbox=dict(facecolor='white', alpha=0.6))

plt.show()
