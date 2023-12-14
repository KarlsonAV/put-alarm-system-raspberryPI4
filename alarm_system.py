import os
import logging
import time
import sys

from camera import Camera
from motion_sensor import MotionSensor
from sound_sensor import SoundSensor

logging.getLogger().setLevel(logging.INFO)


class AlarmSystem:
    def __init__(self, pin_motion_sensor: int, pin_sound_sensor: int) -> None:
        self.motion_sensor = MotionSensor(pin=pin_motion_sensor)
        self.sound_sensor = SoundSensor(pin=pin_sound_sensor)
        self.sound_detection_count = 0
        self.last_sound_detection_time = 0
        self.is_active = False

    def _motion_detected(self, channel: int) -> None:
        logging.info("Motion Detected")
        self.take_photo(output_path=os.path.join("static", "photos", "test.jpeg"))

    def _sound_detected(self, channel: int) -> None:
        logging.info("Sound Detected")
        current_time = time.time()

        if current_time - self.last_sound_detection_time > 0.5:
            # Reset the count if more than half second has passed since the last detection
            self.sound_detection_count = 0

        self.sound_detection_count += 1
        self.last_sound_detection_time = current_time

        if self.sound_detection_count == 2:
            logging.info("Two consecutive sound detections within 1 second. Deactivating the alarm system.")
            self.deactivate()

    def take_photo(self, output_path: str) -> None:
        Camera.take_photo(output_path)

    def activate(self) -> None:
        self.is_active = True
        logging.info("Alarm system activated")
        try:
            self.motion_sensor.detect_motion(motion_detected_callback=self._motion_detected)
            self.sound_sensor.detect_sound(sound_detected_callback=self._sound_detected)

            while self.is_active:
                pass

        except KeyboardInterrupt:
            logging.info("Ctrl+C pressed. Stopping the alarm system.")
            self.deactivate()

    def deactivate(self) -> None:
        self.is_active = False
        logging.info("Alarm system is deactivated")
    

if __name__ == "__main__":
    alarm_system = AlarmSystem(pin_motion_sensor=23, pin_sound_sensor=24)
    alarm_system.activate()
