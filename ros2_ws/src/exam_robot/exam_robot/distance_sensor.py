#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist


class DistanceSensor(Node):
    def __init__(self):
        super().__init__("distance_sensor")
        self.distance = 3.0
        self.linear_x = 0.0

        self.publisher = self.create_publisher(Float32, "/distance", 10)
        self.create_subscription(Twist, "/cmd_vel", self.cmd_callback, 10)
        self.create_timer(0.2, self.publish_distance)

        self.get_logger().info("distance_sensor started")

    def cmd_callback(self, msg: Twist) -> None:
        self.linear_x = msg.linear.x

    def publish_distance(self) -> None:
        if self.linear_x == 0.0:
            self.distance = 3.0
        elif self.linear_x > 0.0:
            self.distance -= 0.2
        else:
            self.distance += 0.2

        self.distance = max(0.5, min(3.0, self.distance))

        msg = Float32()
        msg.data = float(self.distance)
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = DistanceSensor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
