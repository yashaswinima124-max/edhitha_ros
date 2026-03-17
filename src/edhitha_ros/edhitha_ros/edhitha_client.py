#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class DroneClient(Node):

    def __init__(self):
        super().__init__('drone_client')

        self.client = self.create_client(Trigger, 'takeoff_forward')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for drone service...")

    def send_request(self):

        command = input(
            "Enter command (example: forward 2 | left 1 | x 3 y 2 z 2): "
        )

        # simple parsing for display
        words = command.split()

        if words[0] in ["forward", "back", "left", "right"]:
            direction = words[0]
            distance = words[1]
            print(f"Command received → Move {direction} {distance} meters")

        elif words[0] == "x":
            x = words[1]
            y = words[3]
            z = words[5]
            print(f"Command received → Move to position ({x},{y},{z})")

        else:
            print("Unknown command format")

        req = Trigger.Request()

        future = self.client.call_async(req)

        rclpy.spin_until_future_complete(self, future)

        response = future.result()

        print("Server response:", response.message)


def main(args=None):

    rclpy.init(args=args)

    node = DroneClient()

    node.send_request()

    rclpy.shutdown()


if __name__ == '__main__':
    main()