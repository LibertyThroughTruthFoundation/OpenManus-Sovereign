#!/bin/bash
# SOVEREIGN AGENT LAUNCH SCRIPT
# Launches OpenManus-Sovereign with NationOS Ark binding

echo "=========================================="
echo "LAUNCHING SOVEREIGN AGENT"
echo "NationOS - OpenManus-Sovereign"
echo "=========================================="
echo ""

# Check if NationOS Ark is present
if [ ! -d "nationos_ark" ]; then
    echo "[ERROR] NationOS Ark not found. Cannot launch sovereign agent."
    exit 1
fi

echo "[COVENANT] NationOS Ark detected."
echo "[COVENANT] Loading theological framework..."
echo ""

# Use the sovereign configuration
export OPENMANUS_CONFIG="config/config.sovereign.toml"

# Launch the agent
python3 main.py "$@"
