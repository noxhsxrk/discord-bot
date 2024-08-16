#!/bin/bash

# Define the name of the zip file
ZIP_FILE="archive.zip"

# Zip all files in the current directory, excluding specified files and directories
zip -r $ZIP_FILE ./* -x "Makefile" "__pycache__/*" ".gitignore" "scripts/*" "README.md" "src/__pycache__/*"

echo "All files in the current directory have been zipped into $ZIP_FILE, excluding specified files."