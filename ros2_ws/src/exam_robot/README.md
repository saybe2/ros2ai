# Exam Robot

ROS 2 Jazzy training project for the exam task "Basic ROS 2 skills".

## Architecture

Nodes in package `exam_robot`:

- `battery_node`
  - Publishes `/battery_level` (`std_msgs/msg/Float32`) at 1 Hz.
  - Battery starts at 100 and decreases by `discharge_rate` every second.
- `distance_sensor`
  - Subscribes to `/cmd_vel` (`geometry_msgs/msg/Twist`).
  - Publishes `/distance` (`std_msgs/msg/Float32`) at 5 Hz.
- `status_display`
  - Subscribes to `/battery_level` and `/distance`.
  - Publishes `/robot_status` (`std_msgs/msg/String`) at 2 Hz.
- `robot_controller`
  - Subscribes to `/robot_status`.
  - Publishes `/cmd_vel` (`geometry_msgs/msg/Twist`) at 10 Hz.

Standard ROS 2 nodes started by launch:

- `robot_state_publisher` (publishes TF and `/robot_description` from URDF)
- `joint_state_publisher` (publishes `/joint_states`)
- `rviz2` (optional visualization)

## Node/topic diagram

```text
                /battery_level
 battery_node ----------------------+
                                    |
                                    v
                /distance       status_display        /robot_status
 distance_sensor -------------------------------> -------------------+
     ^                                                            |
     |                                                            v
     +------------------------- /cmd_vel ------------------ robot_controller

 robot_state_publisher -> /robot_description, /tf, /tf_static
 joint_state_publisher  -> /joint_states
 rviz2                  -> visualizes RobotModel + TF
```

## Repository structure

```text
ros2_ws/src/exam_robot/
├── exam_robot/
│   ├── battery_node.py
│   ├── distance_sensor.py
│   ├── robot_controller.py
│   └── status_display.py
├── launch/robot_system.launch.py
├── rviz/exam_robot.rviz
├── urdf/exam_robot.urdf
├── package.xml
├── setup.py
└── README.md
```

## Build

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build --packages-select exam_robot
source install/setup.bash
```

## Run

Default run (with RViz):

```bash
ros2 launch exam_robot robot_system.launch.py
```

Run with custom parameters:

```bash
ros2 launch exam_robot robot_system.launch.py \
  discharge_rate:=1.2 \
  max_speed:=0.35 \
  start_rviz:=true
```

Run without RViz:

```bash
ros2 launch exam_robot robot_system.launch.py start_rviz:=false
```

## Testing commands

Open a second terminal and source ROS:

```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

Check nodes:

```bash
ros2 node list
```

Check required topics:

```bash
ros2 topic list | grep -E "^/battery_level$|^/distance$|^/robot_status$|^/cmd_vel$|^/robot_description$|^/joint_states$"
```

Check publish rates:

```bash
ros2 topic hz /battery_level
ros2 topic hz /distance
ros2 topic hz /robot_status
ros2 topic hz /cmd_vel
```

Check message flow:

```bash
ros2 topic echo /battery_level
ros2 topic echo /distance
ros2 topic echo /robot_status
ros2 topic echo /cmd_vel
```

Check TF tree:

```bash
ros2 run tf2_tools view_frames
ls -1 frames*.pdf
```

Expected TF frames include:

- `base_link`
- `left_wheel`
- `right_wheel`
- `sensor_link`

## RViz

RViz config file:

```text
rviz/exam_robot.rviz
```

Expected displays:

- Fixed Frame: `base_link`
- `RobotModel`
- `TF` (axes visible)
