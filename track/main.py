import time

from robomaster import robot


def sub_data_handler(sub_info):
    io_data, ad_data = sub_info
    # print(f"ad value: {ad_data[4]} {ad_data[5]}")  # [4] right sensor & [5] left sensor
    print(f"ad values: {ad_data}")


def main():
    pass


if __name__ == '__main__':
    main()
