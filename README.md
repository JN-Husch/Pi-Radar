# Pi Radar

Pi Radar is a Python project to display basic ADS-B information from a local receiver on a Raspberry Pi.


## Hardware Suggestions

The harware below is used for the development of the Pi Radar. Other Hardware might also work...

- Raspberry Pi 4 (Pi 5 is not recommended in combination with the round 5in WaveShare display due to the supplied connectors not correctly matching the Pi 5)
- Round 5in WaveShare Display (https://www.waveshare.com/5inch-1080x1080-lcd.htm)

### 3D Printed Parts

The case for the Pi Radar has been 3D printed. Files, required hardware and information about the 3D printed case can be found on [Printables](https://www.printables.com/model/847901-wall-mounted-case-for-round-waveshare-5in-display) or [MakerWorld](https://makerworld.com/en/models/433318#profileId-338029).


## Software Installation

To install, follow these steps:

1. Install Rasperry Pi OS (64-bit) Desktop onto your Pi's SD card.


2. Copy the content of this GitHub onto your Pi's Desktop in a folder called "Radar" (without the "").


3. Adjust the radar.cfg file:

   - FEEDER_URL= must contain the path to your receiver's aircraft.json file

   - LAT= and LNG= should be set to your desired radar location


4. Copy the radar.desktop file to `home/pi/.config/autostart/`

5. Reboot the Pi - On startup Pi Radar should show up automatically.
