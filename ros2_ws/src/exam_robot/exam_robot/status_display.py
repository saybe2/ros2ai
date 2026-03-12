#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String


class StatusDisplay(Node):
    def __init__(self):
        super().__init__("status_display")
        self.battery = 100.0
        self.distance = 3.0
        self.last_status = None

        self.publisher = self.create_publisher(String, "/robot_status", 10)
        self.create_subscription(Float32, "/battery_level", self.battery_callback, 10)
        self.create_subscription(Float32, "/distance", self.distance_callback, 10)
        self.create_timer(0.5, self.publish_status)

        self.get_logger().info("status_display started")

    def battery_callback(self, msg: Float32) -> None:
        self.battery = msg.data

    def distance_callback(self, msg: Float32) -> None:
        self.distance = msg.data

    def publish_status(self) -> None:
        if self.battery < 10.0 or self.distance < 0.7:
            status = "CRITICAL"
        elif self.battery < 20.0:
            status = "WARNING: Low battery"
        elif self.distance < 1.0:
            status = "WARNING: Obstacle close"
        else:
            status = "ALL OK"

        msg = String()
        msg.data = status
        self.publisher.publish(msg)

        if status != self.last_status:
            self.get_logger().info(f"Status changed: {status}")
            self.last_status = status


def main(args=None):
    rclpy.init(args=args)
    node = StatusDisplay()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
