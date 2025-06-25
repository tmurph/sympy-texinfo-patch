#!/bin/bash

# Check if exactly one argument is provided
if [ $# -ne 1 ]; then
  echo "Usage: $0 <path-to-info-file>"
  exit 1
fi

INFO_FILE="$1"

# Check if file exists
if [ ! -f "$INFO_FILE" ]; then
  echo "Error: File '$INFO_FILE' does not exist"
  exit 1
fi

# Get absolute path
INFO_FILE_ABS=$(realpath "$INFO_FILE")

# Call emacsclient to create a new frame with the info file
emacsclient --no-wait --alternate-editor= --create-frame --eval "
(progn
  (ignore-errors (kill-buffer \"*sympy-texinfo-patch*\"))
  (info \"($INFO_FILE_ABS)\" \"*sympy-texinfo-patch*\")
  (set-window-dedicated-p (selected-window) t))
"
