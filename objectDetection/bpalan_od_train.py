import subprocess
import mlflow
import os

def train_yolov5(data_yaml_path, epochs=50, output_dir="../final_models/objectDetection/V1", log_file="train.log"):
    experiment_name = "YOLOv5_TrafficSign_Training"
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("data_yaml_path", data_yaml_path)
        mlflow.log_param("output_dir", output_dir)

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
            subprocess.run(cmd, stdout=f_log, stderr=subprocess.STDOUT)

        # Log artifacts
        mlflow.log_artifact(log_file)

        # Optionally log best model
        best_model_path = os.path.join(output_dir, "traffic_sign_model", "weights", "best.pt")
        if os.path.exists(best_model_path):
            mlflow.log_artifact(best_model_path, artifact_path="model")

if __name__ == "__main__":
    train_yolov5("../datasets/traffic_signs/data.yaml", epochs=1)
