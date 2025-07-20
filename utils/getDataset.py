import os
import logging
import shutil
from roboflow import Roboflow

# Setup directories
BASE_DIR = os.path.abspath(os.getcwd())
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.txt")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
DOWNLOAD_DIR = os.path.join(BASE_DIR, "datasets")

os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# Logging configuration
log_file_path = os.path.join(LOGS_DIR, "getDataset.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
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
    logger.info("🚀 Starting dataset download workflow...")

    api_key = get_roboflow_api_key(CREDENTIALS_PATH)
    logger.info(f"✅ Using API key: {api_key}")
    if not api_key:
        logger.error("❌ API key not found or unreadable.")
        return None

    target_path = os.path.join(DOWNLOAD_DIR, "traffic_signs")

    # Remove existing folder before download
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
        logger.info(f"♻️ Removed existing dataset folder: {target_path}")

    try:
        logger.info("🔐 Initializing Roboflow client...")
        rf = Roboflow(api_key=api_key)
        project = rf.workspace("prashant-qp3sw").project("traffic-sign-yh4bz")
        version = project.version(3)

        logger.info("⬇️ Downloading dataset using Roboflow SDK...")
        # Download directly into target_path
        dataset = version.download("yolov7", location=target_path)

        logger.info(f"✅ Dataset downloaded to: {target_path}")
        logger.info(f"📄 Files in dataset: {os.listdir(target_path)}")
        return target_path

    except Exception as e:
        logger.error(f"🔥 Error downloading dataset: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None

# Optional: export logs dir for Streamlit
LOGS_DIR_PATH = LOGS_DIR
