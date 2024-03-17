import csv
import robomaster


def get_ad_data(port_id: int, port: int):
    adc: int = ep_sensor_adaptor.get_adc(id=port_id, port=port)
    print(f"Sensor adapter {port_id}-{port} adc is {adc}.")
    return adc


def drive_handler(right: int, mid: int, left: int):
    if right < 700 & mid > 700 & left < 700:  # robot drives on track
        ep_chassis.move(x=0.05, y=0, z=0, xy_speed=0.4).wait_for_completed()

    elif right > 700 & mid < 700 & left < 700:  # robot drives to the right of the track
        ep_chassis.move(x=0.05, y=0.025, z=0, xy_speed=0.4).wait_for_completed()

    elif right < 700 & mid < 700 & left > 700:  # robot drives to the left of the track
        ep_chassis.move(x=0.05, y=-0.025, z=0, xy_speed=0.4).wait_for_completed()

    else:  # position of robot unknown
        print("No track found.")


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

    while True:
        right_sensor: int = get_ad_data(1, 1)
        mid_sensor: int = get_ad_data(1, 2)
        left_sensor: int = get_ad_data(2, 1)

        drive_handler(right_sensor, mid_sensor, left_sensor)

        write_data_in_csv(track_data_file, track_data_file_headers, {"right_sensor": right_sensor, "mid_sensor":
            mid_sensor, "left_sensor": left_sensor})


if __name__ == '__main__':
    ep_robot = robomaster.robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_chassis = ep_robot.chassis
    ep_sensor_adaptor = ep_robot.sensor_adaptor

    main()

    ep_robot.close()
