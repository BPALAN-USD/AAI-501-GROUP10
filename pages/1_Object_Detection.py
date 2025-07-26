import streamlit as st
import os
from utils.getDataset import get_traffic_dataset
from utils.logger_setup import get_logger
from utils.triggerTraining import run_objectDetection_training_in_background
import pandas as pd
from PIL import Image

# === APP SETUP ===
st.set_page_config(page_title="Traffic Sign ML Workflow", layout="wide")

# === CONFIGURATION ===
DATASET_DIR = "./datasets/traffic_signs/" 
TRAINEDMODEL_DIR = "./final_models/objectDetection/V1/traffic_sign_model/weights/"
RESULTS_CSV = "./results/objectDetection/test/traffic_sign_predictions.csv"

# === HELPERS ===
def dataset_exists() -> bool:
    return os.path.exists(DATASET_DIR) and len(os.listdir(DATASET_DIR)) > 0

def trainmodel_exists() -> bool:
    return os.path.exists(TRAINEDMODEL_DIR) and len(os.listdir(TRAINEDMODEL_DIR)) > 0

def load_results_csv(path):
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        st.error(f"Error reading results file: {e}")
        return None

def render_image_table(df, page_size=6, images_per_row=3):
    # Get unique processed images
    unique_images = df['processed_image'].unique()
    total_records = len(unique_images)
    total_pages = (total_records + page_size - 1) // page_size

    page_num = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)

    start_idx = (page_num - 1) * page_size
    end_idx = min(start_idx + page_size, total_records)
    paginated_images = unique_images[start_idx:end_idx]

    st.write(f"Showing records {start_idx + 1} to {end_idx} of {total_records}")
    st.markdown("---")

    for i in range(0, len(paginated_images), images_per_row):
        cols = st.columns(images_per_row)
        for j in range(images_per_row):
            if i + j >= len(paginated_images):
                break

            image_path_raw = paginated_images[i + j]
            image_path = image_path_raw.replace("../results", "./results")

            with cols[j]:
                try:
                    # Show image once
                    image = Image.open(image_path)
                    st.image(image, use_column_width=True)

                    # Get all rows for this image
                    rows_for_image = df[df['processed_image'] == image_path_raw]

                    # Show info for all detections below the image
                    st.markdown("**Detections:**")
                    for idx, row in rows_for_image.iterrows():
                        label = row.get("name", "N/A")
                        confidence = round(float(row.get("confidence", 0)), 4)
                        st.markdown(f"- **Label:** {label} | **Confidence:** {confidence}")

                except Exception:
                    st.warning("Image not found or unreadable.")
        st.markdown("---")



# === LOGGER SETUP ===
if "object_detection_logger_initialized" not in st.session_state:
    objectDetection_logger = get_logger("object_detection.log")
    objectDetection_logger.info("Object Detection App Started.")
    st.session_state.object_detection_logger_initialized = True
else:
    objectDetection_logger = get_logger("object_detection.log")

# === SESSION STATE INITIALIZATION ===
if "dataset_path" not in st.session_state:
    st.session_state.dataset_path = DATASET_DIR if dataset_exists() else None

if "trainmodel_path" not in st.session_state:
    st.session_state.trainmodel_path = TRAINEDMODEL_DIR if trainmodel_exists() else None

# === RESTART WORKFLOW FUNCTION ===
def restart_workflow():
    st.session_state.dataset_path = None
    st.experimental_rerun()

# === UI SETUP ===
st.markdown("""
    <style>
    .restart-btn-container {
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 100;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚦 Traffic Sign Detection Workflow")

tabs = st.tabs([
    "Step 1: Download Dataset",
    "Step 2: Train YOLOv7 Model",
    "Step 3: Evaluate & Export"
])

# === TAB LOGIC ===
for i, tab in enumerate(tabs):
    with tab:
        st.progress((i + 1) / 3)

        # Step 1: Download Dataset
        if i == 0:
            st.header("Step 1: Download Dataset")

            if dataset_exists():
                st.success(f"Dataset already downloaded at: `{DATASET_DIR}`. You can proceed to training.")
                st.write("You can re-download the dataset if you want to refresh it.")

                if st.button("Re-download Dataset"):
                    with st.spinner("Downloading Traffic dataset..."):
                        try:
                            dataset_path = get_traffic_dataset(objectDetection_logger)
                            if dataset_path and os.path.exists(dataset_path):
                                st.session_state.dataset_path = dataset_path
                                st.success(f"Downloaded to: {dataset_path}")
                            else:
                                st.error("Download finished but dataset path invalid.")
                        except Exception as e:
                            st.error(f"Failed to download: {e}")
            else:
                st.info("Dataset not found on disk. Please download it now.")
                if st.button("Download Dataset"):
                    with st.spinner("Downloading Traffic dataset..."):
                        try:
                            dataset_path = get_traffic_dataset(objectDetection_logger)
                            if dataset_path and os.path.exists(dataset_path):
                                st.session_state.dataset_path = dataset_path
                                st.success(f"Downloaded to: {dataset_path}")
                            else:
                                st.error("Download finished but dataset path invalid.")
                        except Exception as e:
                            st.error(f"Failed to download: {e}")

        # Step 2: Train YOLOv7 Model
        elif i == 1:
            st.header("Step 2: Train YOLOv7 Model")

            if trainmodel_exists():
                st.success(f"Trained model already exists at: `{TRAINEDMODEL_DIR}`. You can proceed to evaluation.")
                st.write("You can re-train the model if you want to refresh it.")

            if not dataset_exists():
                st.warning("Dataset not found on disk. Please download the dataset in Step 1 before training.")
            else:
                st.info(f"Using dataset at: `{DATASET_DIR}`")

                epochs = st.number_input("Epochs", min_value=1, max_value=1000, value=1, step=1)
                batch_size = st.number_input("Batch size", min_value=1, max_value=128, value=16, step=1)

                if st.button("Start Training"):
                    with st.spinner("Triggering training in background..."):
                        try:
                            run_objectDetection_training_in_background(
                                epochs=str(epochs),
                                batch_size=str(batch_size)
                            )
                            st.success("Training triggered in background!")
                        except Exception as e:
                            st.error(f"Failed to trigger training: {e}")

        # Step 3: Evaluate & Export
        elif i == 2:
            st.header("Step 3: Evaluate & Export")

            if not trainmodel_exists():
                st.warning("Trained model not found on disk. Please train the model in Step 2 before evaluating.")
            else:
                st.success(f"Trained model found at: `{TRAINEDMODEL_DIR}`")
                if os.path.exists(RESULTS_CSV):
                    st.subheader("Evaluation Results Table")

                    df_results = load_results_csv(RESULTS_CSV)
                    if df_results is not None and not df_results.empty:
                        render_image_table(df_results, page_size=10)
                    else:
                        st.warning("Results file is empty or malformed.")
                else:
                    st.info("Evaluation results CSV not found yet. It will be available after training completes and evaluation runs.")
