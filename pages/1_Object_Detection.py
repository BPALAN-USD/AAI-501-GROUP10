import streamlit as st
from utils.getDataset import *
import os
from utils.logger_setup import *

st.set_page_config(page_title="Traffic Sign ML Workflow", layout="wide")

if "object_detection_logger_initialized" not in st.session_state:
    objectDetection_logger = get_logger("object_detection.log")
    objectDetection_logger.info("Object Detection App Started.")
    st.session_state.object_detection_logger_initialized = True
else:
    objectDetection_logger = get_logger("object_detection.log")  # reuse the logger


# --- Add Restart Workflow Button in Sidebar ---
def reset():
    st.session_state.step = 1
    st.session_state.dataset_path = None

st.button("🔄 Restart Workflow", on_click=reset)



# Initialize state
if "step" not in st.session_state:
    st.session_state.step = 1
if "dataset_path" not in st.session_state:
    st.session_state.dataset_path = None

# Navigation Header
st.title("🚦 Traffic Sign Detection Workflow")
st.progress(st.session_state.step / 4)

# Step Navigation Logic
def next_step():
    st.session_state.step += 1

def reset():
    st.session_state.step = 1
    st.session_state.dataset_path = None

# Step 1: Download Dataset
if st.session_state.step == 1:
    st.header("Step 1: Download Dataset")

    if st.button("Download Dataset"):
        with st.spinner("Downloading Traffic dataset..."):
            try:
                dataset_path = get_traffic_dataset(objectDetection_logger)
                if dataset_path and os.path.exists(dataset_path):
                    st.session_state.dataset_path = dataset_path
                    st.success(f"Downloaded to: {dataset_path}")
                next_step()
            except Exception as e:
                st.error(f"Failed to download: {e}")

# Step 2: Preview Dataset
elif st.session_state.step == 2:
    st.header("Step 2: Preview Dataset")
    st.info(f"Dataset located at: {st.session_state.dataset_path}")
    
    # Add preview logic here (e.g., display image samples, data summary)
    st.write("✅ Sample preview goes here...")
    if st.button("Continue to Training"):
        next_step()

# Step 3: Train Model
elif st.session_state.step == 3:
    st.header("Step 3: Train YOLOv7 Model")
    st.write("Set hyperparameters and start training...")

    # Add training UI components (e.g., batch size, epochs)
    if st.button("Start Training"):
        with st.spinner("Training model..."):
            # Add training logic
            st.success("Training completed!")
            next_step()

# Step 4: Evaluate & Export
elif st.session_state.step == 4:
    st.header("Step 4: Evaluate & Export")
    st.write("✅ Show evaluation metrics, download trained weights, etc.")

    if st.button("Restart Workflow"):
        reset()

