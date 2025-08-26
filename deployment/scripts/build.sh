#!/bin/bash
set -e

echo "🔨 Building NeuroInsight Hub Enterprise..."

# Build Docker image
docker build -t neuroscreen-workplace:latest .

# Tag for registry
docker tag neuroscreen-workplace:latest ghcr.io/remichenouri/neuroscreen-workplace:latest

echo "✅ Build completed successfully!"
