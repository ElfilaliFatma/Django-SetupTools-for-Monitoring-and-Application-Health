import numpy as np
from sklearn.ensemble import IsolationForest

def detect_anomalies_with_ai(values):
    """
    Detect if the latest value is an anomaly using IsolationForest.
    Returns True if anomaly is detected, else False.
    """
    if len(values) < 10:
        return False  

  
    X = np.array(values).reshape(-1, 1)


    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    model.fit(X)

   
    predictions = model.predict(X)

  
    return predictions[-1] == -1
