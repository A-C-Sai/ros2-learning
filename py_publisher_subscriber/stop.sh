#!/usr/bin/env bash
rm -rf build install log
pkill vglclient
docker rmi $(docker images | awk '{print $1}' | grep -E "vsc*" 2>/dev/null) 2>/dev/null 
osascript -e 'quit app "XQuartz"'
osascript -e 'quit app "Docker Desktop"'
