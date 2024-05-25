import time
import random
import pandas as pd
from matplotlib.animation import FuncAnimation

from robomaster import robot
import matplotlib.pyplot as plt
from itertools import count

drive_counter: int = 0


def animate(i: int):
    x_vals.append(next(index))

    voltage: float = get_ad_data(1, 1) * (12.6 / 1024)
    current: float = get_ad_data(1, 2) * (12.6 / 1024)

    power: float = (voltage * current) * 100

    power_list.append((power * 12.6) / 1000)

    plt.legend(["Power graph"])
    plt.xlabel("time")
    plt.ylabel("miliwatts")

    plt.cla()
    plt.plot(x_vals, power_list)

    plt.legend(["power"])
    plt.xlabel("time")
    plt.ylabel("Watts")

    plt.tight_layout()
    plt.show()

    drive_handler_backwards()


def plot_recorded_data():
    plt.style.use('fivethirtyeight')

    plt.cla()
    ani = FuncAnimation(plt.gcf(), animate)

    plt.tight_layout()
    plt.show()


def get_ad_data(port_id: int, port: int):
    adc: int = ep_sensor_adaptor.get_adc(id=port_id, port=port)
    # print(f"Sensor adapter {port_id}-{port} adc is {adc}.")
    return adc


def drive_handler_forward():
    ep_chassis.move(x=0.15, y=0, z=0, xy_speed=0.15).wait_for_completed()


def drive_handler_left():
    ep_chassis.move(x=0, y=0.15, z=0, xy_speed=0.15).wait_for_completed()


def drive_handler_backwards():
    ep_chassis.move(x=-0.15, y=0, z=0, xy_speed=0.15).wait_for_completed()


def drive_handler_right():
    ep_chassis.move(x=0, y=-0.15, z=0, xy_speed=0.15).wait_for_completed()


def main():
    i: int = 0

    while True:
        if i == 10:
            return False

        # drive_handler()
        plot_recorded_data()

        i += 1


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_chassis = ep_robot.chassis
    ep_sensor_adaptor = ep_robot.sensor_adaptor

    index = count()

    x_vals: list = []

    power_list: list = []
    temperature_left_list: list = []
    temperature_right_list: list = []

    main()

    ep_robot.close()
