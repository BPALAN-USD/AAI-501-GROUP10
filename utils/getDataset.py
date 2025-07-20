from roboflow import Roboflow

def get_traffic_dataset():
    rf = Roboflow(api_key="o3tzxXf3QWaNoIohCmS3")
    project = rf.workspace("prashant-qp3sw").project("traffic-sign-yh4bz")
    version = project.version(3)
    dataset = version.download("yolov7")
                