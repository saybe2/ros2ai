#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist


class RobotController(Node):
    def __init__(self):
        super().__init__("robot_controller")
        self.battery = 100.0
        self.distance = 2.0

        self.publisher = self.create_publisher(Twist, "/cmd_vel", 10)
        self.create_subscription(Float32, "/battery_level", self.battery_callback, 10)
        self.create_subscription(Float32, "/distance", self.distance_callback, 10)
        self.create_timer(0.2, self.publish_cmd_vel)

        self.get_logger().info("robot_controller started")

    def battery_callback(self, msg: Float32) -> None:
        self.battery = msg.data

    def distance_callback(self, msg: Float32) -> None:
        self.distance = msg.data

    def publish_cmd_vel(self) -> None:
        cmd = Twist()

        if self.battery < 10.0:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            mode = "LOW_BATTERY_STOP"
        elif self.distance < 0.5:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.6
            mode = "TURN"
        else:
            cmd.linear.x = 0.25
            cmd.angular.z = 0.0
            mode = "FORWARD"

        self.publisher.publish(cmd)
        self.get_logger().info(
            f"mode={mode}, cmd=({cmd.linear.x:.2f}, {cmd.angular.z:.2f})"
        )


def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

