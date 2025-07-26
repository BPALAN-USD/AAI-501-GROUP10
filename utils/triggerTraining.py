import subprocess

def run_objectDetection_training_in_background(epochs="1", batch_size="16"):
    cmd = [
        "python", "./objectDetection/yolov5/train.py",
        "--img", "416",
        "--batch", batch_size,
        "--epochs", epochs,
        "--data", "./datasets/traffic_signs/data.yaml",  # or full path to your data.yaml
        "--weights", "yolov5s.pt",
        "--name", "traffic_sign_model",
        "--project", "../final_models/objectDetection/V1"
    ]
    # Redirect logs to a file if you want
    log_file = open("./logs/object_detection_training_log.txt", "w")
    subprocess.Popen(cmd, stdout=log_file, stderr=subprocess.STDOUT)