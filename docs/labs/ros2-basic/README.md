# ROS 2 Basic Publisher-Subscriber Lab

This lab guides you through creating a simple ROS 2 publisher and subscriber in Python.

## Learning Objectives

- Create a ROS 2 Python package.
- Write a publisher node that sends "Hello World" messages.
- Write a subscriber node that receives and prints "Hello World" messages.
- Run both nodes and observe communication.

## Prerequisites

- Ubuntu 22.04 LTS
- ROS 2 Humble Hawksbill installed
- A ROS 2 workspace (e.g., `~/ros2_ws`)

## Instructions

### 1. Create a ROS 2 Package

First, navigate to your ROS 2 workspace `src` directory:

```bash
cd ~/ros2_ws/src
```

Now, create a new ROS 2 Python package named `my_ros2_pkg`:

```bash
ros2 pkg create --build-type ament_python my_ros2_pkg
```

### 2. Create the Publisher Node

Navigate into your new package's directory:

```bash
cd my_ros2_pkg
```

Create a new Python file named `publisher_member_function.py` in the `my_ros2_pkg/my_ros2_pkg` directory (the inner `my_ros2_pkg` is where your Python modules reside).

Add the following content to `publisher_member_function.py`:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 3. Create the Subscriber Node

Create a new Python file named `subscriber_member_function.py` in the same `my_ros2_pkg/my_ros2_pkg` directory.

Add the following content to `subscriber_member_function.py`:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 4. Update `setup.py`

You need to tell ROS 2 about your executables. Open `my_ros2_pkg/setup.py` and modify the `entry_points` section. It should look like this:

```python
from setuptools import setup

package_name = 'my_ros2_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/resource', ['resource/' + package_name]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name', # <--- CHANGE THIS
    maintainer_email='your_email@example.com', # <--- CHANGE THIS
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = my_ros2_pkg.publisher_member_function:main',
            'listener = my_ros2_pkg.subscriber_member_function:main',
        ],
    },
)

```
**Remember to change `maintainer` and `maintainer_email`**.

### 5. Build Your Package

Navigate back to your ROS 2 workspace root:

```bash
cd ~/ros2_ws
```

Build your package:

```bash
colcon build --packages-select my_ros2_pkg
```

Source your workspace:

```bash
source install/setup.bash
```

### 6. Run the Nodes

Open two separate terminal windows.

In the first terminal, run the publisher:

```bash
ros2 run my_ros2_pkg talker
```

In the second terminal, run the subscriber:

```bash
ros2 run my_ros2_pkg listener
```

You should see "Hello World" messages being published in the first terminal and received in the second terminal.

## Troubleshooting

-   **`Package 'my_ros2_pkg' not found`**: Ensure you have sourced your workspace correctly (`source install/setup.bash`).
-   **No messages received**: Check that both nodes are running, and that they are using the same topic name (`topic` in this case). Use `ros2 topic list` to see active topics.
-   **Python errors**: Double-check your Python code for typos and correct indentation.
