from __future__ import print_function

import hid
import time

# Instead of lsusb you can also use this to find the device
# enumerate USB devices
# for d in hid.enumerate():
#     keys = list(d.keys())
#     keys.sort()
#     for key in keys:
#         print("%s : %s" % (key, d[key]))
#     print()

print("Opening the device")

h = hid.Device(vid=0x16c0,pid=0x0480)

print("Manufacturer: %s" % h.manufacturer)
print("Product: %s" % h.product)

shortsize = 2 # 16/8 
tempoffset = 4

try:
    while True:
        buf = h.read(64)
        # uncomment this to see full packet
        # print('read: "{}"'.format(buf))

        if len(buf) == 64:
            pwr = "Extern" if buf[2] else "Parasite"


            temp = int.from_bytes(buf[tempoffset:tempoffset+shortsize],byteorder="little",signed=True)
            temp /= 10.0

            hexid = "0x "
            for b in buf[0x08:0x10]:
                hexb = hex(b)[2:]
                if len(hexb) == 1: 
                    hexb = f"0{hexb}" # pad with 0
                hexid += f"{hexb} "

            print(f"Sensor #{buf[1]} of {buf[0]}: {temp}C Power: {pwr} ID: {hexid}")

finally:
    print("Closing the device")
    h.close()
