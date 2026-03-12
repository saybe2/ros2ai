# Exam Robot

## Build

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select exam_robot
source install/setup.bash
```

## Run

```bash
ros2 launch exam_robot robot_system.launch.py
```

## Quick checks

```bash
ros2 node list
ros2 topic list
ros2 topic echo /battery_level
ros2 topic echo /distance
ros2 topic echo /robot_status
ros2 topic echo /cmd_vel
```

