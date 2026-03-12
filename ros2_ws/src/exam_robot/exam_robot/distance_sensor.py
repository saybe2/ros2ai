#!/usr/bin/env python3

import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist


class DistanceSensor(Node):
    def __init__(self):
        super().__init__("distance_sensor")
        self.distance = 2.5
        self.linear_x = 0.0

        self.publisher = self.create_publisher(Float32, "/distance", 10)
        self.create_subscription(Twist, "/cmd_vel", self.cmd_callback, 10)
        self.create_timer(0.2, self.publish_distance)

        self.get_logger().info("distance_sensor started")

    def cmd_callback(self, msg: Twist) -> None:
        self.linear_x = msg.linear.x

    def publish_distance(self) -> None:
        if self.linear_x > 0.01:
            self.distance -= 0.03
        else:
            self.distance += 0.01

        self.distance += random.uniform(-0.01, 0.01)
        self.distance = max(0.2, min(3.0, self.distance))

        if self.distance <= 0.25:
            self.distance = 2.0

        msg = Float32()
        msg.data = float(self.distance)
        self.publisher.publish(msg)

        self.get_logger().info(f"distance={self.distance:.2f} m")


def main(args=None):
    rclpy.init(args=args)
    node = DistanceSensor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

