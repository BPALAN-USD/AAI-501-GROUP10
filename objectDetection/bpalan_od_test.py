import torch
import os
from pathlib import Path
from PIL import Image
import pandas as pd

# Load your trained model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/traffic_sign_model2/weights/best.pt')

# Set folder path for test images
test_folder = '../datasets/traffic_signs/test/images/'  # e.g., './test_images/'

# Create output directory
output_folder = '../results/objectDetection/test/'
os.makedirs(output_folder, exist_ok=True)

# List to hold all predictions
all_predictions = []

# Loop through images in the test folder
for img_file in os.listdir(test_folder):
    if img_file.lower().endswith(('.jpg', '.jpeg', '.png')) and not img_file.lower().startswith("test"):
        img_path = os.path.join(test_folder, img_file)
        print(f"Processing image: {img_path}")
        model.conf = 0.02 
        results = model(img_path)

        # Save annotated image to output folder
        results.save(save_dir=output_folder)

        df = results.pandas().xyxy[0]
        if not df.empty:
            df['source_image'] = img_path
            df['processed_image'] = os.path.join(output_folder, img_file)
            df = df[['source_image','processed_image', 'name', 'confidence', 'xmin', 'ymin', 'xmax', 'ymax']]  # Cleaned output
            all_predictions.append(df)
        else:
            print(f"No Object Detected for : {img_path}")
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


# Final DataFrame
final_df = pd.concat(all_predictions, ignore_index=True)

# Save as CSV
csv_output_path = os.path.join(output_folder, 'traffic_sign_predictions.csv')
final_df.to_csv(csv_output_path, index=False)

print(f"\n✅ Predictions CSV saved at: {csv_output_path}")

# -----------------------------
# Analysis of detection results
# -----------------------------

# Reload the CSV to ensure reading saved results
df = pd.read_csv(csv_output_path)

# Mark detected rows where 'name' is not None or 'None'
df['detected'] = df['name'].notnull() & (df['name'] != 'None')

# Total unique source images processed
total_images = df['source_image'].nunique()

# Number of images with at least one detection
images_with_detection = df[df['detected']]['source_image'].nunique()

# Number of images with no detections
images_without_detection = total_images - images_with_detection

print(f"\n--- Detection Summary ---")
print(f"Total images processed: {total_images}")
print(f"Images with detections: {images_with_detection}")
print(f"Images with NO detections: {images_without_detection}")

# Detection rate percentage
detection_rate = (images_with_detection / total_images) * 100
print(f"Detection rate: {detection_rate:.2f}%")

# Count of detections per class (ignoring 'None' classes)
class_counts = df[df['detected']]['name'].value_counts()

print("\nDetections per class:")
print(class_counts)
