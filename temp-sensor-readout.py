from __future__ import print_function

import hid
import time
import argparse

parser = argparse.ArgumentParser("simple_example")
parser.add_argument("--sensor_id", help="If set, will only display data from that sensor", type=int, default=None)
parser.add_argument('--verbose', dest='verbose', action='store_true')
parser.add_argument('--no-verbose', dest='verbose', action='store_false')
parser.set_defaults(feature=True)

args = parser.parse_args()

# Instead of lsusb you can also use this to find the device
# enumerate USB devices
# for d in hid.enumerate():
#     keys = list(d.keys())
#     keys.sort()
#     for key in keys:
#         print("%s : %s" % (key, d[key]))
#     print()

if args.verbose:
    print("Opening the device")

h = hid.Device(vid=0x16c0,pid=0x0480)

if args.verbose:
    print("Manufacturer: %s" % h.manufacturer)
    print("Product: %s" % h.product)
    print(f"selected: sensor_id {args.sensor_id}, verbose: {args.verbose}")

shortsize = 2 # 16/8 
tempoffset = 4


try:
    while True:
        buf = h.read(64)
        # uncomment this to see full packet
        # print('read: "{}"'.format(buf))

        if len(buf) == 64:
            sensor_sum = buf[0]
            sensor_num = buf[1]

            if args.sensor_id is sensor_num or args.sensor_id is None:

                temp = int.from_bytes(buf[tempoffset:tempoffset+shortsize],byteorder="little",signed=True)
                temp /= 10.0

                pwr = ""
                hexid = ""
                if args.verbose:
                    pwr = "Powersource: " + ("Extern" if buf[2] else "Parasite")
                    hexid = "Sensor ID: 0x "
                    for b in buf[0x08:0x10]:
                        hexb = hex(b)[2:]
                        if len(hexb) == 1: 
                            hexb = f"0{hexb}" # pad with 0
                        hexid += f"{hexb} "

                if args.verbose:
                    print(f"Sensor #{sensor_num} of {sensor_sum}: {temp}C | {pwr} | {hexid}")
                elif args.sensor_id is None:
                    print(f"#{sensor_num}/{sensor_sum}: {temp}C")
                else:
                    print(f"{temp}")

finally:
    print("Closing the device")
    h.close()
