#!/usr/bin/env bash
rm -rf build install log .vscode
pkill vglclient
docker stop ros2_jazzy
echo "waiting for container to be removed to delete image..."
while docker ps -a --format '{{.Names}}' | grep -q "ros2_jazzy"; do
	sleep 1
done
sleep 5
echo "deleting image..."
docker rmi $(docker images --format '{{.Repository}}:{{.Tag}}' | grep "^vsc-") 2>/dev/null
osascript -e 'quit app "Docker Desktop"'
osascript -e 'quit app "XQuartz"'


