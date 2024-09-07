# RunBook for Deploying and Testing Flask Microservices

## Overview

This RunBook outlines the steps to deploy and test a Python Flask microservices application using Docker, Kubernetes (AWS EKS), and GitHub Actions. It includes setting up the environment, configuring CI/CD pipelines, and executing tests.

## Prerequisites

- **Python Version:** 3.12 or higher
- **Flask Version:** 2.0.3
- **Werkzeug Version:** 2.0.3
- **pytest Version:** 7.4.2
- **Flask-JWT-Extended Version:** 4.3.1
- **Docker**
- **Kubernetes (AWS EKS)**
- **GitHub Actions**

## Project Structure

- `services/`
  - `crypto-price-service/`
  - `app.py`
  - `Dockerfile`
  - `requirements.txt`
  - `__init__.py`
  - `test/`
    - `__init__.py`
    - `test_app.py`
  - `transaction-service/`
    - `app.py`
    - `Dockerfile`
    - `requirements.txt`
    - `__init__.py`
    - `test/`
      - `__init__.py`
      - `test_app.py`
  - `account-service/`
    - `app.py`
    - `Dockerfile`
    - `requirements.txt`
    - `__init__.py`
    - `test/`
      - `__init__.py`
      - `test_app.py`
- `kubernetes/`
  - `blue-green/`
    - `crypto-price-service-blue-deployment.yaml`
    - `crypto-price-service-green-deployment.yaml`
    - `transaction-service-blue-deployment.yaml`
    - `transaction-service-green-deployment.yaml`
    - `account-service-blue-deployment.yaml`
    - `account-service-green-deployment.yaml`
    - `crypto-price-service-service.yaml`
    - `transaction-service-service.yaml`
    - `account-service-blue-service.yaml`
  - `namespace.yaml`
- `.github/`
  - `workflows/`
    - `ci-cd-pipeline.yml`

## Environment Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/NethmiKaumudi/coinbase-exchange-solution-NK.git
   cd coinbase-exchange-solution-NK
   ```

2. ## Pipeline Configuration

The pipeline configuration is defined in a GitHub Actions workflow file (`.github/workflows/ci-cd-pipeline.yml`). The following sections describe the steps involved in the pipeline.

### Workflow Triggers

The workflow is triggered on:

- `push` to the `main` branch
- `pull_request` targeting the `main` branch

### Jobs

#### Build and Test

This job performs the following steps:

Note: Ensure you add the following secrets in your GitHub repository settings under Settings > Secrets > Actions:

DOCKER_USERNAME (Docker Hub username)
DOCKER_PASSWORD (Docker Hub password)
KUBE_CONFIG (Kubeconfig for accessing the Kubernetes cluster)
KUBE_CONTEXT (Kubeconfig context to use)

1. **Checkout Code**

   ````yaml
   - name: Checkout code
     uses: actions/checkout@v2
   2, **Set up Docker Buildx**
   ```yaml
   - name: Set up Docker Buildx
     uses: docker/setup-buildx-action@v2

   ````

3, **Log in to Docker Hub**

- name: Log in to Docker Hub
  run: echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin

4, **Build and Push Docker Images**

- name: Build and Push Docker Images
  run: |
  services=("crypto-price-service" "transaction-service" "account-service")
  for service in "${services[@]}"; do
      docker build -t ${{ secrets.DOCKER_USERNAME }}/$service:latest ./services/$service
      docker push ${{ secrets.DOCKER_USERNAME }}/$service:latest
  done

5,**Install Dependencies and Run Unit Tests**

- name: Install Dependencies and Run Unit Tests
  run: |
  services=("crypto-price-service" "transaction-service" "account-service")
  for service in "${services[@]}"; do
      cd services/$service
  pip install -r requirements.txt
  pytest
  cd ../..
  done

6, **Run Integration Tests**

- name: Run Integration Tests
  run: |
  docker run -d --name crypto-price-service -p 5001:5001 ${{ secrets.DOCKER_USERNAME }}/crypto-price-service:latest
  docker run -d --name transaction-service -p 5002:5002 ${{ secrets.DOCKER_USERNAME }}/transaction-service:latest
  docker run -d --name account-service -p 5003:5003 ${{ secrets.DOCKER_USERNAME }}/account-service:latest
  sleep 30
  curl -f http://localhost:5001/crypto-prices || exit 1
  curl -f http://localhost:5002/transactions || exit 1
  curl -f http://localhost:5003/accounts || exit 1
  docker stop crypto-price-service transaction-service account-service
  docker rm crypto-price-service transaction-service account-service

7,** Set up kubeconfig**

## Set up Kubernetes (AWS EKS)

Ensure your EKS cluster is running:

Go to ** AWS Console > EKS ** and follow steps to create a cluster.
Set up your KUBECONFIG and KUBE_CONTEXT locally:

- name: Set up kubeconfig
  run: |
  echo "${{ secrets.KUBE_CONFIG }}" > $HOME/.kube/config
  kubectl config use-context ${{ secrets.KUBE_CONTEXT }}

8, **Deploy to Kubernetes (Blue-Green Deployment)**

- name: Deploy to Kubernetes (Blue-Green Deployment)
  run: |
  services=("crypto-price-service" "transaction-service" "account-service")
  namespace="default"
  for service in "${services[@]}"; do
      # Create/update blue deployment
      kubectl apply -f kubernetes/blue-green/$service-blue-deployment.yaml --namespace=$namespace
      # Create/update green deployment
      kubectl apply -f kubernetes/blue-green/$service-green-deployment.yaml --namespace=$namespace

      # Switch the service to the green deployment
      kubectl patch service $service -p '{"spec":{"selector":{"version":"green"}}}' --namespace=$namespace

  done

9, **Clean up**

- name: Clean up
  run: |
  docker system prune -af

3. ### Testing

## Running Unit Tests Locally

To run the unit tests locally, navigate to the root directory of each service and execute:

-pytest

\*\*indide cicd pipe do aotomation testing

### Summary of Changes

1. **Fixed Formatting Issues:** Corrected YAML indentation and formatting to ensure the steps are properly outlined.
2. **Clarified Secrets Information:** Added instructions for adding secrets in GitHub repository settings.
3. **Adjusted File Names and Paths:** Ensured consistent use of paths and file names throughout the document.

Feel free to adjust the file names and paths to match your project structure. This runbook provides a clear outline of the CI/CD pipeline and helps maintain consistency across deployments.

# Troubleshooting Guide

### Error: Kubernetes Pods Not Starting

- **Check pod logs for errors:**
  ```bash
  kubectl logs <pod_name>
  ```
- **Ensure that `KUBECONFIG` and `KUBE_CONTEXT` are properly set.**

---

### Error: Docker Image Not Found

- **Ensure the Docker image is correctly tagged and pushed:**
  ```bash
  docker images | grep <service_name>
  docker push <docker_username>/<service_name>:latest
  ```

---

### Error: Service Not Accessible

- **Verify the service is correctly exposed:**
  ```bash
  kubectl get services
  ```

---

### Test Failures

- **Run the tests locally and check for:**
  - Python-related issues
  - Incorrect API endpoints in integration tests
