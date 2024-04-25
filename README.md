# Pi Radar

Pi Radar is a Python project to display basic ADS-B information from a local receiver on a Raspberry Pi.

There are several different styles of radar scopes available:

![Radar_Example](https://github.com/JN-Husch/Pi-Radar/assets/156305491/3c46a59e-bdc7-491c-96d8-f99feeb98f57)

</br>

## Hardware Suggestions

The harware below is used for the development of the Pi Radar. Other Hardware might also work...

- Raspberry Pi 4 (Pi 5 is not recommended in combination with the round 5in WaveShare display due to the supplied connectors not correctly matching the Pi 5)
- Round 5in WaveShare Display (https://www.waveshare.com/5inch-1080x1080-lcd.htm)

### 3D Printed Parts

The case for the Pi Radar has been 3D printed. Files, required hardware and information about the 3D printed case can be found on [Printables](https://www.printables.com/model/847901-wall-mounted-case-for-round-waveshare-5in-display) or [MakerWorld](https://makerworld.com/en/models/433318#profileId-338029).

</br>

## Software Installation

### Raspberry Pi OS:

To install, follow these steps:

1. Install Rasperry Pi OS (64-bit) Desktop onto your Pi's SD card.

2. Create a folder called "Radar" on the Desktop of your Pi.

3. Download the latest Pi-Radar release for Raspberry and Linux from here: https://github.com/JN-Husch/Pi-Radar/releases/

4. Unzip the contents from the Pi-Radar download into the folder on your Desktop.

5. Adjust the `radar.cfg` file:

   - FEEDER_URL= must contain the path to your receiver's aircraft.json file

   - LAT= and LNG= should be set to your desired radar location

Optional:

5. Copy the radar.desktop file to `home/pi/.config/autostart/`

6. Reboot the Pi - On startup Pi Radar should show up automatically.


</br>

### Windows

To run, follow these steps:

1. Download the latest Pi-Radar release for Windows from here: https://github.com/JN-Husch/Pi-Radar/releases/

2. Unzip the folder to any location.

3. Adjust the radar.cfg file:

   - FEEDER_URL= must contain the path to your receiver's aircraft.json file

   - LAT= and LNG= should be set to your desired radar location

4. Run Pi-Radar by clicking on the Pi-Radar.exe

Note: The `res` folder and the `radar.cfg` file must be in the same location as the Pi-Radar.exe
