#!/bin/bash

# Load .env file
if [ -f .env ]; then
    export $(cat .env | sed 's/#.*//g' | xargs)
fi

# Check the value of DEVELOPMENT key
if [ "$DEVELOPMENT" == "true" ]; then
    echo "Starting development script..."
    python3 button_trial.py
else
    echo "Starting production script..."
    python3 button_integration.py
fi

# Start Flask app in a separate screen session
screen -dmS python3 app.py 

echo "Flask app started in a separate screen session."
