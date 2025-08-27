#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from paho.mqtt.client import Client as MQTTClient

import math
import os
import sys
import time
import threading

from  arm_robot_bridge import ArmRobot

class ArmRobotMqttBridge:
    def __init__(self, mqtt_host, mqtt_port):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        # self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(mqtt_host, mqtt_port, 60)
        # self.mqtt_client.loop_start()
        self.setup_armrobot()
        self.mqtt_client.loop_forever()
        
    def setup_armrobot(self):
        self.robot = ArmRobot()

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print('Connection Success' if rc == 0 else 'Connection refuse')
        if rc == 0:
            client.subscribe("task_start") 
            client.subscribe("task_stop") 
            client.subscribe("get_state") 
                

    def on_disconnect(self,client, userdata, rc):
        if  rc != 0:
           print("Unexpected disconnection.")

    def on_message(self, client, userdata, msg):
        """
        サブスクライブ時のコールバック関数
        """
        if msg.topic == "task_start":
            time.sleep(1)
            while self.robot.project_run :
                time.sleep(1)
                print("タスク実行中")
            self.robot.set_project(msg.payload.decode("utf-8"))
            time.sleep(1)
            self.robot.task_start()
            print("タスク開始メッセージ受信")
        elif msg.topic == "task_stop":
            self.robot.task_stop()
            print("タスク停止メッセージ受信")
        elif msg.topic == "get_state":
            self.robot.get_state()
            print("状態表示")

    def run(self):        
        # print("ArmRobot MQTT Bridge 起動")
        self.mqtt_client.loop_forever()


if __name__ == "__main__":
    mqtt_host = "localhost"                             # MQTTブローカーのIPアドレス
    mqtt_port = 1883                                    # ポート番号：1883
    node = ArmRobotMqttBridge(mqtt_host, mqtt_port)
    node.run()
