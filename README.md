# Project README

## Overview

This project involves designing and implementing a container-based solution for managing and monitoring services for the Coinbase crypto exchange. It includes setting up a CI/CD pipeline, deploying services using Kubernetes on AWS EKS, and automating testing processes.

## Table of Contents

- [Project Description](#project-description)
- [Prerequisites](#prerequisites)
- [Deployment Steps](#deployment-steps)
  - [Build and Push Docker Images](#build-and-push-docker-images)
  - [Deploy to AWS EKS](#deploy-to-aws-eks)
  - [Run Automated Tests](#run-automated-tests)
- [Rollback Procedure](#rollback-procedure)
- [CI/CD Pipeline](#cicd-pipeline)
- [Testing](#testing)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Project Description

This project aims to create a highly available and secure container-based service solution for Coinbase using Kubernetes and AWS EKS. The solution features Blue-Green deployment for zero-downtime updates and automated testing after every deployment.

## Prerequisites

- **AWS EKS Cluster:** Set up and accessible.
- **Docker Hub Account:** For storing Docker images.
- **GitHub Repository:** For managing code and CI/CD pipeline.
- **Kubernetes Manifests:** Blue-Green deployment configuration files.
- **Secrets:** Docker credentials and kubeconfig stored in GitHub secrets.

## Deployment Steps

### Build and Push Docker Images

1. **Trigger Pipeline:**
   - Commit to the `main` branch or open a pull request to trigger the CI/CD pipeline.

2. **Pipeline Actions:**
   - Checkout code.
   - Build Docker images for each microservice.
   - Push Docker images to Docker Hub.

### Deploy to AWS EKS

1. **Set Up kubeconfig:**
   - Ensure `kubectl` is configured with the correct Kubernetes context.

2. **Apply Kubernetes Manifests:**
   - **Deploy Blue Environment:**
     ```bash
     kubectl apply -f kubernetes/blue-green/crypto-price-service-blue-deployment.yaml --namespace=default
     kubectl apply -f kubernetes/blue-green/transaction-service-blue-deployment.yaml --namespace=default
     kubectl apply -f kubernetes/blue-green/account-service-blue-deployment.yaml --namespace=default
     ```
   - **Deploy Green Environment:**
     ```bash
     kubectl apply -f kubernetes/blue-green/crypto-price-service-green-deployment.yaml --namespace=default
     kubectl apply -f kubernetes/blue-green/transaction-service-green-deployment.yaml --namespace=default
     kubectl apply -f kubernetes/blue-green/account-service-green-deployment.yaml --namespace=default
     ```
   - **Switch Traffic to Green Deployment:**
     ```bash
     kubectl patch service crypto-price-service -p '{"spec":{"selector":{"version":"green"}}}' --namespace=default
     kubectl patch service transaction-service -p '{"spec":{"selector":{"version":"green"}}}' --namespace=default
     kubectl patch service account-service -p '{"spec":{"selector":{"version":"green"}}}' --namespace=default
     ```

### Run Automated Tests

- **Integration Tests:**
  - Automatically triggered by the CI/CD pipeline.
  - Verify service accessibility and functionality using HTTP requests.

- **Manual Verification:**
  - Check service status:
    ```bash
    kubectl get services --namespace=default
    ```
  - Check pods:
    ```bash
    kubectl get pods --namespace=default
    ```
  - Verify endpoints:
    ```bash
    curl -f http://<service-ip>:<port>/crypto-prices
    curl -f http://<service-ip>:<port>/transactions
    curl -f http://<service-ip>:<port>/accounts
    ```

## Rollback Procedure

1. **Switch Traffic to Blue Deployment:**
   ```bash
   kubectl patch service crypto-price-service -p '{"spec":{"selector":{"version":"blue"}}}' --namespace=default
   kubectl patch service transaction-service -p '{"spec":{"selector":{"version":"blue"}}}' --namespace=default
   kubectl patch service account-service -p '{"spec":{"selector":{"version":"blue"}}}' --namespace=default


## Documentation
  Runbook: Available in the repository root, detailing deployment and testing procedures.