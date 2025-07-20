import streamlit as st
from utils.getDataset import *
import os


st.set_page_config(page_title="Traffic Sign ML Workflow", layout="wide")

# Clear all log files at the start of the app
logs_directory = os.path.join(os.path.dirname(__file__), "logs")
if os.path.exists(logs_directory):
    for f in os.listdir(logs_directory):
        file_path = os.path.join(logs_directory, f)
        if os.path.isfile(file_path):
            os.remove(file_path)

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
                dataset = get_traffic_dataset()
                st.session_state.dataset_path = dataset.location
                st.success(f"Downloaded to: {dataset.location}")
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

# --- LOG FILES VIEWER ---
logs_directory = os.path.join(os.path.dirname(__file__), "logs")
if os.path.exists(logs_directory):
    log_files = [f for f in os.listdir(logs_directory) if os.path.isfile(os.path.join(logs_directory, f))]
    if log_files:
        with st.expander("Show Log Files"):
            tabs = st.tabs(log_files)
            for i, log_file in enumerate(log_files):
                with tabs[i]:
                    log_path = os.path.join(logs_directory, log_file)
                    with open(log_path, "r") as f:
                        st.code(f.read(), language="log")