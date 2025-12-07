# URDF Robot Modeling Lab

This lab guides you through creating a simple humanoid URDF (Unified Robot Description Format) model and visualizing it in RViz2.

## Learning Objectives

- Understand the basic structure of a URDF file.
- Define links and joints to create a robot's kinematic structure.
- Add visual and collision properties to robot links.
- Visualize your URDF model in RViz2.

## Prerequisites

- Ubuntu 22.04 LTS
- ROS 2 Humble Hawksbill installed
- A ROS 2 workspace (e.g., `~/ros2_ws`)

## Instructions

### 1. Create a ROS 2 Package for your URDF

Navigate to your ROS 2 workspace `src` directory:

```bash
cd ~/ros2_ws/src
```

Create a new ROS 2 ament_cmake package named `simple_humanoid_description`:

```bash
ros2 pkg create --build-type ament_cmake simple_humanoid_description
```

### 2. Create the URDF File

Inside your `simple_humanoid_description` package, create a new directory named `urdf`:

```bash
mkdir -p simple_humanoid_description/urdf
```

Navigate into the `urdf` directory:

```bash
cd simple_humanoid_description/urdf
```

Create a new file named `simple_humanoid.urdf` and add the following content:

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">

  <!-- Base Link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.2 0.2 0.1"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 0.8 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.2 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Torso Link -->
  <link name="torso_link">
    <visual>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
      <material name="green">
        <color rgba="0 0.8 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.5"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Head Link -->
  <link name="head_link">
    <visual>
      <geometry>
        <sphere radius="0.08"/>
      </geometry>
      <material name="red">
        <color rgba="0.8 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.08"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.2"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Base to Torso Joint -->
  <joint name="base_to_torso_joint" type="fixed">
    <parent link="base_link"/>
    <child link="torso_link"/>
    <origin xyz="0 0 0.2"/>
  </joint>

  <!-- Torso to Head Joint -->
  <joint name="torso_to_head_joint" type="revolute">
    <parent link="torso_link"/>
    <child link="head_link"/>
    <origin xyz="0 0 0.2"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="100"/>
  </joint>

</robot>
```

### 3. Update `package.xml`

Open `simple_humanoid_description/package.xml` and ensure it has the following dependencies (if not already present):

```xml
  <depend>rviz2</depend>
  <depend>xacro</depend>
  <exec_depend>robot_state_publisher</exec_depend>
  <exec_depend>joint_state_publisher</exec_depend>
  <exec_depend>joint_state_publisher_gui</exec_depend>
```

### 4. Build Your Package

Navigate back to your ROS 2 workspace root:

```bash
cd ~/ros2_ws
```

Build your package:

```bash
colcon build --packages-select simple_humanoid_description
```

Source your workspace:

```bash
source install/setup.bash
```

### 5. Visualize in RViz2

To visualize your URDF model, you'll need to run `robot_state_publisher`, `joint_state_publisher_gui`, and `rviz2`.

Open a terminal and run the `robot_state_publisher` and `joint_state_publisher_gui`:

```bash
ros2 launch simple_humanoid_description display.launch.py model:=$(ros2 pkg prefix simple_humanoid_description)/share/simple_humanoid_description/urdf/simple_humanoid.urdf
```
**Note**: You might need to create a `display.launch.py` file in your package's `launch` directory.

Alternatively, you can manually run the components:

Open three separate terminals:

**Terminal 1 (Robot State Publisher):**
```bash
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="`cat $(ros2 pkg prefix simple_humanoid_description)/share/simple_humanoid_description/urdf/simple_humanoid.urdf`"
```

**Terminal 2 (Joint State Publisher GUI):**
```bash
ros2 run joint_state_publisher_gui joint_state_publisher_gui
```

**Terminal 3 (RViz2):**
```bash
rviz2
```

In RViz2, add a "RobotModel" display. If you don't see anything, ensure the "Fixed Frame" in RViz2 is set to `base_link` (or another link in your robot).

You should now see your simple humanoid robot! You can manipulate the joint values using the sliders in the `joint_state_publisher_gui` window.

## Troubleshooting

-   **URDF not loading in RViz2**: Ensure `robot_state_publisher` is running and the `robot_description` parameter is set correctly. Check RViz2's "RobotModel" status for errors.
-   **No sliders in `joint_state_publisher_gui`**: Ensure `joint_state_publisher_gui` is running and your URDF has revolute/prismatic joints.
