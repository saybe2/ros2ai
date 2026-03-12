#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String
from geometry_msgs.msg import Twist


class StatusDisplay(Node):
    def __init__(self):
        super().__init__("status_display")
        self.battery = 100.0
        self.distance = 2.0
        self.cmd_linear = 0.0
        self.cmd_angular = 0.0

        self.publisher = self.create_publisher(String, "/robot_status", 10)
        self.create_subscription(Float32, "/battery_level", self.battery_callback, 10)
        self.create_subscription(Float32, "/distance", self.distance_callback, 10)
        self.create_subscription(Twist, "/cmd_vel", self.cmd_callback, 10)
        self.create_timer(1.0, self.publish_status)

        self.get_logger().info("status_display started")

    def battery_callback(self, msg: Float32) -> None:
        self.battery = msg.data

    def distance_callback(self, msg: Float32) -> None:
        self.distance = msg.data

    def cmd_callback(self, msg: Twist) -> None:
        self.cmd_linear = msg.linear.x
        self.cmd_angular = msg.angular.z

    def publish_status(self) -> None:
        if self.battery < 10.0:
            state = "LOW_BATTERY"
        elif self.distance < 0.5:
            state = "OBSTACLE"
        elif abs(self.cmd_linear) > 0.01 or abs(self.cmd_angular) > 0.01:
            state = "MOVING"
        else:
            state = "IDLE"

        status = (
            f"state={state}; battery={self.battery:.1f}%; "
            f"distance={self.distance:.2f}m; "
            f"cmd=({self.cmd_linear:.2f}, {self.cmd_angular:.2f})"
        )

        msg = String()
        msg.data = status
        self.publisher.publish(msg)
        self.get_logger().info(status)


def main(args=None):
    rclpy.init(args=args)
    node = StatusDisplay()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

