#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class BatteryNode(Node):
    def __init__(self):
        super().__init__("battery_node")
        self.level = 100.0
        self.next_log_level = 90.0

        self.declare_parameter("discharge_rate", 1.0)
        self.discharge_rate = float(self.get_parameter("discharge_rate").value)
        if self.discharge_rate < 0.0:
            self.get_logger().warning("discharge_rate < 0.0, reset to 0.0")
            self.discharge_rate = 0.0

        self.publisher = self.create_publisher(Float32, "/battery_level", 10)
        self.create_timer(1.0, self.publish_battery)

        self.get_logger().info(
            f"battery_node started (discharge_rate={self.discharge_rate:.2f}%/s)"
        )

    def publish_battery(self) -> None:
        self.level = max(0.0, self.level - self.discharge_rate)

        msg = Float32()
        msg.data = float(self.level)
        self.publisher.publish(msg)

        while self.level <= self.next_log_level:
            self.get_logger().info(f"Battery: {int(self.next_log_level)}%")
            self.next_log_level -= 10.0


def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
