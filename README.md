# Django Monitoring System with Celery, Prometheus, and AI Anomaly Detection

This project is a comprehensive monitoring solution built with Django that integrates:

* **Celery** and **Celery Beat** for asynchronous and periodic tasks
* **Prometheus** and **Windows Exporter** for system metrics collection
* **Alertmanager** for real-time alerts
* **AI-based anomaly detection** using Isolation Forest

It provides REST and GraphQL endpoints to manage metrics, visualize trends, and alert on unusual behaviors.

---



## Features

* Define and store metrics with integrity constraints
* REST API and GraphQL for metric ingestion and querying
* Periodic Prometheus data fetching using Celery Beat
* Anomaly detection using Isolation Forest
* Alerting on threshold breaches using Prometheus + Alertmanager
* Token-based secured endpoints with CORS enabled

---

## Architecture Overview

```text
Windows Exporter (metrics) --> Prometheus --> Celery Beat (schedule scrape)
                                         |--> Celery Worker (push to DB)
                                                             |--> Anomaly Detection (AI)
                                                             |--> Alerts --> Alertmanager --> Notification
```

---

## Technologies Used

* **Django**: Backend framework
* **Django REST Framework (DRF)**: REST API support
* **Graphene-Django**: GraphQL support
* **Celery + Celery Beat**: Background and periodic task management
* **Redis**: Celery message broker
* **Prometheus**: Time-series metrics collection
* **Windows Exporter**: System metrics provider for Windows
* **Alertmanager**: Alert notifications
* **scikit-learn**: AI anomaly detection (Isolation Forest)

---

## Installation and Setup

1. **Clone the Repository**:

```bash
git clone https://github.com/ElfilaliFatma/Django-SetupTools-for-Monitoring-and-Application-Health.git
cd monitoring
```

2. **Create Virtual Environment**:

```bash
python -m venv venv
source venv/bin/activate  
```

3. **Install Dependencies**:

```bash
pip install -r requirements.txt
```

4. **Configure `.env` and Django Settings**

5. **Run Migrations**:

```bash
python manage.py migrate
```

6. **Start Django Server**:

```bash
python manage.py runserver
```

---

## Prometheus Configuration

 `prometheus.yml`:


### Example Prometheus Queries:

* CPU Usage:

```promql
100 - (avg by (instance)(irate(windows_cpu_time_total{mode="idle"}[5m])) * 100)
```

* Memory:

```promql
windows_memory_available_bytes
```

---

## Windows Exporter Setup

1. Download from [Releases](https://github.com/prometheus-community/windows_exporter/releases)
2. Run the executable: it exposes metrics at `http://localhost:9182/metrics`
3. Ensure Prometheus can scrape this target

---

## Celery and Beat Integration

Start Redis as the broker:

```bash
redis-server.exe
```

Start Celery workers:

```bash
celery -A monitoring worker --loglevel=info
```

Start Beat scheduler:

```bash
celery -A monitoring beat --loglevel=info
```

Celery Beat schedules scraping jobs that:

* Query Prometheus
* Store data into Django models
* Run anomaly detection on fresh data

---

## AI Anomaly Detection

Implemented with `IsolationForest` from `scikit-learn`:

```python
from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    model = IsolationForest(contamination=0.05)
    df['anomaly'] = model.fit_predict(df[['value']])
    return df[df['anomaly'] == -1]
```

* This model isolates outliers based on how deep they appear in trees.
* Used to detect unusual spikes/drops in metric trends.

---

## Alertmanager Setup

`alert_rules.yml`:

Start Alertmanager 

---

## Security

* All endpoints are protected with token authentication
* CORS middleware is enabled

---

## Testing

Run test cases using Django test framework:

```bash
python manage.py test
```

Example test includes:

* Validating negative metric rejection
* GraphQL mutation checks
* Celery and Prometheus mocks

---


## Author

**Your Name**
📧 [your.email@example.com](mailto:your.email@example.com)
GitHub: [@yourusername](https://github.com/yourusername)
