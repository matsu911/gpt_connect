#!/bin/bash

PORT=9222
PROFILE="Profile 1"

while getopts "n:p:" opt; do
  case $opt in
    p)
      PORT=$OPTARG
      ;;
    n)
      PROFILE=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

google-chrome-stable --remote-debugging-port=$PORT \
                     --flag-switches-begin \
                     --flag-switches-end \
                     --profile-directory="$PROFILE" \
                     https://chat.openai.com/ &
