import torch
import os
from pathlib import Path
from PIL import Image
import pandas as pd

# === Load the trained model ===
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/traffic_sign_model2/weights/best.pt')
model.conf = 0.02  # Set once globally

# === Set folder path for test images ===
test_folder = '../datasets/traffic_signs/test/images/'

# === Set flat output folder for annotated images ===
output_folder = '../results/objectDetection/test/'
os.makedirs(output_folder, exist_ok=True)

# === List to hold all predictions ===
all_predictions = []

# === Loop through test images ===
for img_file in os.listdir(test_folder):
    if img_file.lower().endswith(('.jpg', '.jpeg', '.png')) and not img_file.lower().startswith("test"):
        img_path = os.path.join(test_folder, img_file)
        print(f"Processing image: {img_path}")
        
        # Inference
        results = model(img_path)

        # Render annotated image
        rendered_img = results.render()[0]  # numpy array (BGR)
        output_img_path = os.path.join(output_folder, img_file)
        Image.fromarray(rendered_img).save(output_img_path)

        # Extract detection results
        df = results.pandas().xyxy[0]
        if not df.empty:
            df['source_image'] = img_path
            df['processed_image'] = output_img_path
            df = df[['source_image', 'processed_image', 'name', 'confidence', 'xmin', 'ymin', 'xmax', 'ymax']]
            all_predictions.append(df)
        else:
            print(f"No Object Detected for: {img_path}")
            all_predictions.append(pd.DataFrame([{
                'source_image': img_path,
                'processed_image': 'None',
                'name': 'None',
                'confidence': 0.0,
                'xmin': None,
                'ymin': None,
                'xmax': None,
                'ymax': None
            }]))

# === Combine all predictions and save as CSV ===
final_df = pd.concat(all_predictions, ignore_index=True)
csv_output_path = os.path.join(output_folder, 'traffic_sign_predictions.csv')
final_df.to_csv(csv_output_path, index=False)

print(f"\n✅ Predictions CSV saved at: {csv_output_path}")

# === Detection Summary ===
df = pd.read_csv(csv_output_path)
df['detected'] = df['name'].notnull() & (df['name'] != 'None')

total_images = df['source_image'].nunique()
images_with_detection = df[df['detected']]['source_image'].nunique()
images_without_detection = total_images - images_with_detection
detection_rate = (images_with_detection / total_images) * 100

print(f"\n--- Detection Summary ---")
print(f"Total images processed: {total_images}")
print(f"Images with detections: {images_with_detection}")
print(f"Images with NO detections: {images_without_detection}")
print(f"Detection rate: {detection_rate:.2f}%")

class_counts = df[df['detected']]['name'].value_counts()
print("\nDetections per class:")
print(class_counts)
