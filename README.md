# Cloud-Native DevOps Project

A learning project implementing a CI/CD platform with Flask, Docker, Jenkins,
Kubernetes, Terraform, AWS, Prometheus, Grafana, and security scanning.

## Run locally

```bash
python -m venv venv
# Activate the environment for your OS
pip install -r app/requirements.txt
pytest
python app/app.py
```

Application endpoints:

- `GET /`
- `GET /health`
- `GET /version`

## Build and run with Docker

```bash
docker build -t cloud-native-devops:1.0 .
docker run --rm -p 5000:5000 cloud-native-devops:1.0
```
