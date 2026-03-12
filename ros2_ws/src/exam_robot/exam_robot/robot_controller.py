#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class RobotController(Node):
    def __init__(self):
        super().__init__("robot_controller")
        self.current_status = "CRITICAL"
        self.current_mode = None

        self.publisher = self.create_publisher(Twist, "/cmd_vel", 10)
        self.create_subscription(String, "/robot_status", self.status_callback, 10)
        self.create_timer(0.1, self.publish_cmd_vel)

        self.get_logger().info("robot_controller started")
        self.update_mode_from_status(self.current_status)

    def status_callback(self, msg: String) -> None:
        self.current_status = msg.data
        self.update_mode_from_status(self.current_status)

    def update_mode_from_status(self, status: str) -> None:
        if status == "ALL OK":
            mode = "ALL_OK_MOVE"
        elif status == "WARNING: Low battery":
            mode = "LOW_BATTERY_SLOW"
        elif status == "WARNING: Obstacle close":
            mode = "OBSTACLE_TURN"
        else:
            mode = "CRITICAL_STOP"

        if mode != self.current_mode:
            self.current_mode = mode
            self.get_logger().info(
                f"Mode changed: {self.current_mode} (status: {status})"
            )

    def publish_cmd_vel(self) -> None:
        cmd = Twist()

        if self.current_mode == "ALL_OK_MOVE":
            cmd.linear.x = 0.3
            cmd.angular.z = 0.0
        elif self.current_mode == "LOW_BATTERY_SLOW":
            cmd.linear.x = 0.1
            cmd.angular.z = 0.0
        elif self.current_mode == "OBSTACLE_TURN":
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5
        else:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        self.publisher.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
