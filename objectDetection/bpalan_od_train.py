import subprocess

def train_yolov5(data_yaml_path, epochs=50):
    cmd = [
        "python", "yolov5/train.py",
        "--img", "416",
        "--batch", "16",
        "--epochs", str(epochs),
        "--data", data_yaml_path,
        "--weights", "yolov5s.pt",
        "--name", "traffic_sign_model"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    train_yolov5("../datasets/traffic_signs/data.yaml", epochs=5)
