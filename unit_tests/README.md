# ROS2 Jazzy — VS Code Dev Container Setup

## Workflow

### 1. Clone workspace
```bash
cp -R ./ros2_ws <dst>
cd ~/ros2_ws
```

### 2. Startup Script
- Run `start.sh`


### 3. Open in Dev Container
1. Open the workspace folder in VS Code (`code .`)
2. VS Code will detect `.devcontainer/` and show a notification
3. Click **"Reopen in Container"** (or `Ctrl+Shift+P` → *Dev Containers: Reopen in Container*)
4. The image builds on first launch (5–15 min depending on your connection) — subsequent opens are fast

### 4. Clean Up Operations
1. Click **"Close Remote Connection"** (or `Ctrl+Shift+P` → *Dev Containers: Close Remote Connection*)
2. Run `stop.sh` on Host Machine
---

## Common Commands

```bash
# Build the workspace (alias defined in .bashrc)
build

# Launch a GUI app (X11 forwarding)
ros2 run rviz2 rviz2

# Launch with VirtualGL acceleration
vglrun ros2 run rviz2 rviz2
```

---

## Troubleshooting

**No GUI / "cannot open display"**
- Confirm your host X server is running and allowing network connections
- macOS XQuartz: run `xhost +localhost` in a host terminal

**Gazebo crash / OpenGL errors**
- Try launching with `vglrun`: `vglrun gazebo`
- Verify `Xvfb :1` is running: `ps aux | grep Xvfb`

**Build fails on first open**
- The `src/` directory may be empty — this is fine. Add your packages and run `build`
- Check the terminal output in VS Code for specific colcon errors
