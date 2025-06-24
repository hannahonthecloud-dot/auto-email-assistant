#!/bin/bash

# Set environment name
ENV_NAME="myemailprojectenv"

# Step 1: Create the environment if it doesn't exist
if [ ! -d "$ENV_NAME" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $ENV_NAME
fi

# Step 2: Activate the environment
echo "Activating virtual environment..."
source $ENV_NAME/bin/activate

# Step 3: Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Run the script
echo "Running email script..."
python send-emails.py
