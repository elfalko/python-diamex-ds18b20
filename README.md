# Simple readout for the USB-Temparatur-Sensor-Tester for DS18B20 by diamex.de
Original sensor and drivers can be found at the [supplier's page](https://www.diamex.de/dxshop/USB-Temperatur-Sensor-Tester-fuer-DS18B20-Rev-C)

## Why
Diamex does not include a prebuild readout program for linux. They include sources for it, but compiling them did not work out of the box for me due to lack of knowledge about hidraw, libusb and their compatibility with WSL2.
I lacked the necessary motivation to get that running.
Also, the codebase in which I will use it is python anyway.

## How to use
1. Clone this repo.
2. Install python and stuff you need.
3. `pip install hid`
4. Set up a udev rule for the device. Place it in `/etc/udev/rules/98-temp-sensor-diamax.rules` or similar. 
```
# e.g. /etc/udev/rules/98-temp-sensor-diamax.rules
SUBSYSTEM=="usb", ATTR{idVendor}=="16c0", ATTR{idProduct}=="0480", MODE="0660", GROUP="plugdev", TAG+="uaccess", TAG+="udev-acl", SYMLINK+="ds18b20%n"
KERNEL=="hidraw*", ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="0480", MODE="0660", GROUP="plugdev", TAG+="uaccess", TAG+="udev-acl"
```
5. Compare the `idVendor` and `idProduct` with your device `lsusb` (although they are presumably the same for all diamex products.
On my machine, the board showed up as this:
```
Bus 003 Device 006: ID 16c0:0480 Van Ooijen Technische Informatica Teensy RawHID
```
If they differ, replace them in both the udev rules and the script.
6. You might need to call `udevadm control --reload-rules` to reload the rules. You might also want to add your user to the `plugdev` group to get access to the device.
7. Run the script
``` bash
python temp-sensor-readout.py
```

The output should look something like this:
``` bash
$ python temp-sensor-readout.py

Opening the device
Manufacturer: DIAMEX GmbH
Product: Temp-Sensor-Tester
Sensor #1 of 2: 24.7C Power: Extern ID: 0x 28 5e bf 79 97 15 03 9b
Sensor #2 of 2: 26.4C Power: Extern ID: 0x 28 aa 11 e2 4b 14 01 0b
Sensor #1 of 2: 24.6C Power: Extern ID: 0x 28 5e bf 79 97 15 03 9b
Sensor #2 of 2: 26.4C Power: Extern ID: 0x 28 aa 11 e2 4b 14 01 0b
Sensor #1 of 2: 24.6C Power: Extern ID: 0x 28 5e bf 79 97 15 03 9b
Sensor #2 of 2: 26.4C Power: Extern ID: 0x 28 aa 11 e2 4b 14 01 0b
Sensor #1 of 2: 24.6C Power: Extern ID: 0x 28 5e bf 79 97 15 03 9b
Sensor #2 of 2: 26.4C Power: Extern ID: 0x 28 aa 11 e2 4b 14 01 0b
[...]
^CClosing the device
```

## License
This is mainly derived from diamex sources and hid tutorial scripts.
From the diamex readme.txt:

> Zur nichtkommerziellen Verwendung dürfen alle Sourcen beliebig modifiziert oder erweitert werden.

Rough translation:
For noncommercial use all sources may be modified or extended in any way.


## Useful links
[supplier's page](https://www.diamex.de/dxshop/USB-Temperatur-Sensor-Tester-fuer-DS18B20-Rev-C)

