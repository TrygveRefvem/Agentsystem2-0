#!/bin/bash

echo "Building Agentsystem 2.0..."
docker-compose build

echo "Starting Agentsystem 2.0..."
docker-compose up
