import os
import shutil
from roboflow import Roboflow

# Setup directories
BASE_DIR = os.path.abspath(os.getcwd())
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.txt")

DOWNLOAD_DIR = os.path.join(BASE_DIR, "datasets")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)



def get_roboflow_api_key(logger,filepath):
    try:
        with open(filepath, "r") as f:
            for line in f:
                if line.startswith("ROBOFLOW_API_KEY="):
                    return line.strip().split("=", 1)[1]
    except Exception as e:
        logger.error(f"Failed to read API key: {e}")
    return None

def get_traffic_dataset(logger):
    logger.info("🚀 Starting dataset download workflow...")

    api_key = get_roboflow_api_key(logger,CREDENTIALS_PATH)
    logger.info(f"✅ Using API key: {api_key}")
    if not api_key:
        logger.error("❌ API key not found or unreadable. Ensure you have a valid credentials.txt file with the format 'ROBOFLOW_API_KEY=your_api_key' in home directory. ")
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
        ##logger.info(f"📄 Files in dataset: {os.listdir(target_path)}")
        return target_path

    except Exception as e:
        logger.error(f"🔥 Error downloading dataset: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None

