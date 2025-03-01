#!/bin/bash

MODULE_NAME="flake8"

if python -c "import ${MODULE_NAME}" &> /dev/null; then
    echo "Found $MODULE_NAME"
else
    echo "Installing $MODULE_NAME..."
    pip install flake8 > /dev/null
fi

echo "Running flake8 for linting..."
flake8 ./

if [ $? -eq 0 ]; then
    echo "No flake8 errors. Proceeding to build."
    echo "Building the images..."
    docker-compose up --build
    echo "Build finised"
else
    echo "There are flake8 errors. Solve them before building."
fi

