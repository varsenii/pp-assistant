#!/bin/bash
set -e

CURRENT_DIR=$(dirname "$(realpath "$0")")
PROJECT_DIR=$(dirname "$CURRENT_DIR")
cd "$PROJECT_DIR"

# Install dependencies for Luxonis devices (e.g., DepthAI)
echo "Installing dependencies for Luxonis devices..."
sudo wget -qO- https://docs.luxonis.com/install_dependencies.sh | bash

# Set udev rules for Movidius devices (e.g., Intel Neural Compute Stick)
echo "Setting udev rules for Movidius devices..."
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
sudo udevadm control --reload-rules && sudo udevadm trigger

# Clone the DepthAI Python library and install its dependencies
echo "Cloning DepthAI Python library and installing dependencies..."
mkdir -p libs
git clone https://github.com/luxonis/depthai-python.git libs/depthai-python
python3 libs/depthai-python/examples/install_requirements.py



