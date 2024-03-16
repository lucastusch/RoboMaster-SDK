import time
import csv
from robomaster import robot


# def sub_data_handler(sub_info):
#     io_data, ad_data = sub_info
#     # print(f"ad value: {ad_data[4]} {ad_data[5]}")  # [4] right sensor & [5] left sensor
#     print(f"ad values: {ad_data}")

def get_ad_data(port_id: int, port: int):
    adc: int = ep_sensor_adaptor.get_adc(id=port_id, port=port)
    print(f"sensor adapter id1-port1 adc is {adc}")
    return adc


def drive_handler(right: int, mid: int, left: int):
    # ep_chassis.move(x=0, y=0, z=0, xy_speed=0.7).wait_for_completed()  # coordinates in m, speed in m/s

    if right < 700 & mid > 700 & left < 700:  # robot drives on track
        ep_chassis.move(x=0.05, y=0, z=0, xy_speed=0.4).wait_for_completed()

    elif right > 700 & mid < 700 & left < 700:  # robot drives to the right of the track
        ep_chassis.move(x=0.05, y=0.025, z=0, xy_speed=0.4).wait_for_completed()

    elif right < 7000 & mid < 700 & left > 700:  # robot drives to the left of the track
        ep_chassis.move(x=0.05, y=-0.025, z=0, xy_speed=0.4).wait_for_completed()


def init_csv(name: str, header: list):
    with open(name, "w", newline="\n") as f:
        writer = csv.DictWriter(f, delimiter=";", fieldnames=header)
        writer.writeheader()


def write_data_in_csv(name: str, header: list, content: dict):
    with open(name, "a", newline="\n") as f:
        writer = csv.DictWriter(f, delimiter=";", fieldnames=header)
        writer.writerow(content)


def main():
    track_data_file: str = "track_data.csv"
    track_data_file_headers: list = ["right sensor", "mid sensor", "left sensor"]
    init_csv(track_data_file, track_data_file_headers)

    measurements_data_file: str = "measurements_data.csv"
    measurements_data_file_headers: list = ["voltage", "current", "temperature left", "temperature right"]
    init_csv(measurements_data_file, measurements_data_file_headers)


    while True:
        right_sensor: int = get_ad_data(1, 1)
        mid_sensor: int = get_ad_data(1, 2)
        left_sensor: int = get_ad_data(2, 1)

        drive_handler(right_sensor, mid_sensor, left_sensor)

        voltage: int = get_ad_data(3, 1)
        current: int = get_ad_data(3, 2)
        temperature_left: int = get_ad_data(4, 1)
        temperature_right: int = get_ad_data(4, 2)

        write_data_in_csv(track_data_file, track_data_file_headers, {"right_sensor": right_sensor, "mid_sensor":
            mid_sensor, "left_sensor": left_sensor})

        write_data_in_csv(track_data_file, track_data_file_headers, {"voltage": voltage, "current":
            current, "temperature left": temperature_left, "temperature right": temperature_right})


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_chassis = ep_robot.chassis
    ep_sensor_adaptor = ep_robot.sensor_adaptor

    main()

    ep_robot.close()
