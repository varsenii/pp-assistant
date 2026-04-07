#!/bin/bash
set -e

CURRENT_DIR=$(dirname "$(realpath "$0")")
PROJECT_DIR=$(dirname "$CURRENT_DIR")

cd "$PROJECT_DIR"

# Create a virtual environment and activate it
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip && pip install -r requirements.txt

# Install dependencies for Luxonis devices and set up udev rules for Movidius devices
echo "Installing dependencies for Luxonis devices and setting up udev rules for Movidius devices..."
./scripts/install_oakd.sh


