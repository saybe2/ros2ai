#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist


class BatteryNode(Node):
    def __init__(self):
        super().__init__("battery_node")
        self.level = 100.0
        self.is_moving = False

        self.publisher = self.create_publisher(Float32, "/battery_level", 10)
        self.create_subscription(Twist, "/cmd_vel", self.cmd_callback, 10)
        self.create_timer(1.0, self.publish_battery)

        self.get_logger().info("battery_node started")

    def cmd_callback(self, msg: Twist) -> None:
        self.is_moving = abs(msg.linear.x) > 0.01 or abs(msg.angular.z) > 0.01

    def publish_battery(self) -> None:
        discharge = 0.8 if self.is_moving else 0.2
        self.level = max(0.0, self.level - discharge)

        msg = Float32()
        msg.data = float(self.level)
        self.publisher.publish(msg)

        self.get_logger().info(f"battery={self.level:.1f}%")


def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

