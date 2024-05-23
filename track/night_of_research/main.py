import time
import robomaster


def get_ad_data(port_id: int, port: int):
    adc: int = ep_sensor_adaptor.get_adc(id=port_id, port=port)
    print(f"Sensor adapter {port_id}-{port} adc is {adc}.")
    return adc


def drive_handler(right: int, mid: int, left: int):
    if right < 303 & mid > 303 & left < 303:  # robot drives on track
        ep_chassis.move(x=0.05, y=0, z=0, xy_speed=0.4).wait_for_completed()

    elif right > 303 & mid < 303 & left < 303:  # robot drives to the right of the track
        ep_chassis.move(x=0.05, y=0.007, z=0, xy_speed=0.4).wait_for_completed()

    elif right < 303 & mid < 303 & left > 303:  # robot drives to the left of the track
        ep_chassis.move(x=0.05, y=-0.007, z=0, xy_speed=0.4).wait_for_completed()

    else:  # robot's position unknown
        print("No track found.")


def main():
    track_data_file_headers: list = ["right sensor", "mid sensor", "left sensor"]

    while True:
        right_sensor: int = get_ad_data(1, 1)
        mid_sensor: int = get_ad_data(1, 2)
        left_sensor: int = get_ad_data(2, 1)

        drive_handler(right_sensor, mid_sensor, left_sensor)

        voltage: int = get_ad_data(3, 1)
        current: int = get_ad_data(3, 2)
        temperature_left: int = get_ad_data(4, 1)
        temperature_right: int = get_ad_data(4, 2)


if __name__ == '__main__':
    ep_robot = robomaster.robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_chassis = ep_robot.chassis
    ep_sensor_adaptor = ep_robot.sensor_adaptor

    main()

    ep_robot.close()
