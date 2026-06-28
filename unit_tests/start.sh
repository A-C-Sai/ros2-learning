#!/usr/bin/env bash
open -a XQuartz && xhost +localhost
open -a "Docker Desktop"
/opt/VirtualGL/bin/vglclient -detach
