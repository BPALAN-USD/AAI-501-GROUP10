import os
import logging
from roboflow import Roboflow

download_directory = "datasets"
credentials_path = os.path.join(os.path.dirname(__file__), "../credentials.txt")
logs_directory = os.path.join(os.path.dirname(__file__), "../logs")
os.makedirs(logs_directory, exist_ok=True)
log_file_path = os.path.join(logs_directory, "getDataset.log")

# Configure logger to write to file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),
        # Remove the next line if you do NOT want logs in the console
        # logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_roboflow_api_key(filepath):
    try:
        with open(filepath, "r") as f:
            for line in f:
                if line.startswith("ROBOFLOW_API_KEY="):
                    return line.strip().split("=", 1)[1]
    except Exception as e:
        logger.error(f"Failed to read API key: {e}")
    return None

def get_traffic_dataset():
    api_key = get_roboflow_api_key(credentials_path)
    logger.info(f"Using API key: {api_key}")
    if not api_key:
        logger.error("API key not found in credentials.txt.")
        return "Error: API key not found in credentials.txt."

    download_path = os.path.join(download_directory, "traffic_signs")
    os.makedirs(download_path, exist_ok=True)
    logger.info(f"Download path: {download_path}")

    try:
        rf = Roboflow(api_key=api_key)
        logger.info("Roboflow initialized.")
        project = rf.workspace("prashant-qp3sw").project("traffic-sign-yh4bz")
        logger.info("Project loaded.")
        version = project.version(3)
        logger.info("Version loaded.")
        dataset = version.download("yolov7", location=download_path)
        logger.info("Dataset downloaded successfully.")
        return dataset
    except Exception as e:
        logger.error(f"Error downloading dataset: {e}")
        return f"Error downloading dataset: {e}"