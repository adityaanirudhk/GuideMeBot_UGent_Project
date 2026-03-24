#!/bin/bash

# Download Whisper model for speech recognition
# This script downloads the base English model (~140MB)

MODEL_FILE="ggml-base.en.bin"
MODEL_URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin"

echo "Downloading Whisper base English model..."
echo "This may take a few minutes (~140MB download)"

if [ -f "$MODEL_FILE" ]; then
    echo "Model file already exists: $MODEL_FILE"
    read -p "Do you want to re-download? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping download."
        exit 0
    fi
    rm "$MODEL_FILE"
fi

wget "$MODEL_URL" -O "$MODEL_FILE"

if [ $? -eq 0 ]; then
    echo "✓ Model downloaded successfully: $MODEL_FILE"
    echo "You can now run: ros2 run guide_me_bot whisper_bridge"
else
    echo "✗ Failed to download model"
    exit 1
fi
