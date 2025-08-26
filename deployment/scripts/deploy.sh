#!/bin/bash
set -e

echo "🚀 Deploying NeuroInsight Hub Enterprise..."

# Apply Kubernetes manifests
kubectl apply -f deployment/k8s/

# Wait for deployment
kubectl rollout status deployment/neuroscreen-app

echo "✅ Deployment completed successfully!"
echo "🌐 Application available at: https://neuroscreen.your-domain.com"
