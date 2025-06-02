import numpy as np

def detect_anomaly(values):
    if len(values) < 10:
        return False 
    mean = np.mean(values)
    std = np.std(values)
    latest = values[-1]
    if std == 0:
        return False
    z_score = (latest - mean) / std
    return abs(z_score) > 3
