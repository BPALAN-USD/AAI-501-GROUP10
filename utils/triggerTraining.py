import subprocess
import mlflow
import os
import time

def run_objectDetection_training_in_background(epochs="1", batch_size="16"):
    data_yaml_path = "./datasets/traffic_signs/data.yaml"
    project_path = "../final_models/objectDetection/V1"
    experiment_name = "YOLOv5_ObjectDetection_Async"

    os.makedirs("./logs", exist_ok=True)
    log_path = "./logs/object_detection_training_log.txt"

    mlflow.set_experiment(experiment_name)

    # Start MLflow run
    with mlflow.start_run() as run:
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("data_yaml_path", data_yaml_path)

        cmd = [
            "python", "./objectDetection/yolov5/train.py",
            "--img", "416",
            "--batch", batch_size,
            "--epochs", epochs,
            "--data", data_yaml_path,
            "--weights", "yolov5s.pt",
            "--name", "traffic_sign_model",
            "--project", project_path
        ]

        with open(log_path, "w") as log_file:
            subprocess.Popen(cmd, stdout=log_file, stderr=subprocess.STDOUT)

        # Log the training log file as an artifact
        # NOTE: This logs an empty file initially if training is still running.
        # You can revisit and log artifacts in a separate step once training finishes.
        mlflow.log_artifact(log_path)

        # Optional: schedule another job to check and log final model weights later
        # e.g., path = f"{project_path}/traffic_sign_model/weights/best.pt"
