#!/usr/bin/env bash

# MongoDB & Python Integration - Quick Start Guide
# This script sets up the environment and runs demonstrations

echo "=================================================="
echo "MongoDB & Python Integration - Quick Start"
echo "=================================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "📥 Activating virtual environment..."
source venv/bin/activate

echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt --default-timeout=1000
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "=================================================="
echo "Available Options:"
echo "=================================================="
echo ""
echo "1. Run CRUD Demo (No MongoDB Required)"
echo "2. Run Full CRUD Examples (Requires MongoDB)"
echo "3. Generate Homework Word Document"
echo "4. Exit"
echo ""

read -p "Select option (1-4): " option

case $option in
    1)
        echo ""
        echo "Running CRUD Demo..."
        echo "=================================================="
        python Python-MongoDB-Integration/crud_demo.py
        ;;
    2)
        echo ""
        echo "Running Full CRUD Examples..."
        echo "Make sure MongoDB is running on localhost:27017"
        echo "=================================================="
        python Python-MongoDB-Integration/crud_examples.py
        ;;
    3)
        echo ""
        echo "Generating Homework Word Document..."
        echo "=================================================="
        python Python-MongoDB-Integration/generate_homework_doc.py
        ;;
    4)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid option"
        exit 1
        ;;
esac

echo ""
echo "✓ Execution completed!"
