import subprocess

def train_yolov5(data_yaml_path, epochs=50, output_dir="../final_models/objectDetection/V1", log_file="train.log"):
    cmd = [
        "python", "yolov5/train.py",
        "--img", "416",
        "--batch", "16",
        "--epochs", str(epochs),
        "--data", data_yaml_path,
        "--weights", "yolov5s.pt",
        "--name", "traffic_sign_model",
        "--project", output_dir
    ]

    with open(log_file, "w") as f_log:
        # Run process and redirect stdout and stderr to log file
        process = subprocess.run(cmd, stdout=f_log, stderr=subprocess.STDOUT)

if __name__ == "__main__":
    train_yolov5("../datasets/traffic_signs/data.yaml", epochs=1)
