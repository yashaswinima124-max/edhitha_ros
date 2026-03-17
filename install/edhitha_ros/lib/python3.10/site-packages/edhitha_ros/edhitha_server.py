#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_srvs.srv import Trigger
from geometry_msgs.msg import PoseStamped
from mavros_msgs.srv import CommandBool, SetMode


class DroneServiceServer(Node):

    def __init__(self):
        super().__init__('drone_service_server')

        # Create service
        self.service = self.create_service(
            Trigger,
            'takeoff_forward',
            self.service_callback
        )

        # Publisher for drone position
        self.publisher = self.create_publisher(
            PoseStamped,
            '/mavros/setpoint_position/local',
            10
        )

        # MAVROS service clients
        self.arm_client = self.create_client(
            CommandBool,
            '/mavros/cmd/arming'
        )

        self.mode_client = self.create_client(
            SetMode,
            '/mavros/set_mode'
        )

        self.get_logger().info("Drone Service Server Ready")

    def service_callback(self, request, response):

        self.get_logger().info("Mission started")

        # ARM DRONE
        self.get_logger().info("Arming drone...")
        arm_req = CommandBool.Request()
        arm_req.value = True
        self.arm_client.call_async(arm_req)

        # SET OFFBOARD MODE
        self.get_logger().info("Switching to OFFBOARD mode...")
        mode_req = SetMode.Request()
        mode_req.custom_mode = "OFFBOARD"
        self.mode_client.call_async(mode_req)

        msg = PoseStamped()

        # TAKEOFF
        self.get_logger().info("Taking off...")

        msg.pose.position.x = 0.0
        msg.pose.position.y = 0.0
        msg.pose.position.z = 2.0

        for i in range(50):
            self.publisher.publish(msg)

        self.get_logger().info("Takeoff completed")

        # MOVE FORWARD
        self.get_logger().info("Moving forward...")

        msg.pose.position.x = 5.0
        msg.pose.position.y = 0.0
        msg.pose.position.z = 2.0

        for i in range(100):
            self.publisher.publish(msg)

        self.get_logger().info("Forward movement completed")

        # Response to client
        response.success = True
        response.message = "Takeoff done and drone moved forward successfully"

        return response


def main(args=None):
    rclpy.init(args=args)

    node = DroneServiceServer()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()