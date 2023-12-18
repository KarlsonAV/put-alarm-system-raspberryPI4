import os
import logging
import time
import concurrent.futures

from datetime import datetime

from camera import Camera
from motion_sensor import MotionSensor
from sound_sensor import SoundSensor
from face_detector import FaceDetector


logging.getLogger().setLevel(logging.INFO)

PIN_MOTION_SENSOR = 23
PIN_SOUND_SENSOR = 24
FACE_DETECTOR_PATH = "haarcascades/haarcascade_frontalface_default.xml"
MAX_THREADS_WORKERS = 5


class AlarmSystem:
    def __init__(self) -> None:
        self.motion_sensor = MotionSensor(pin=PIN_MOTION_SENSOR)
        self.sound_sensor = SoundSensor(pin=PIN_SOUND_SENSOR)
        self.face_detector = FaceDetector(FACE_DETECTOR_PATH)
        self.sound_detection_count = 0
        self.last_sound_detection_time = 0
        self.is_active = False


    def _process_motion_detection(self):
        current_datetime = datetime.now()
        image_path = os.path.join("static", "photos", '_'.join(str(current_datetime).split(' ')))
        image_path += ".jpeg"
        image_path = self.take_photo(output_path=image_path)
        if image_path:
            self.detect_faces(image_path=image_path)

    
    def _motion_detected(self, channel: int) -> None:
        logging.info("Motion Detected")
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS_WORKERS) as executor:
            executor.submit(self._process_motion_detection)


    def _sound_detected(self, channel: int) -> None:
        logging.info("Sound Detected")
        current_time = time.time()

        if current_time - self.last_sound_detection_time > 0.5:
            # Reset the count if more than half second has passed since the last detection
            self.sound_detection_count = 0

        self.sound_detection_count += 1
        self.last_sound_detection_time = current_time

        if self.sound_detection_count == 2:
            logging.info("Two consecutive sound detections within 0.5 second. Deactivating the alarm system.")
            self.deactivate()


    def take_photo(self, output_path: str) -> None:
        return Camera.take_photo(output_path)


    def detect_faces(self, image_path: str) -> None:
        logging.info("Face detection activated")
        number_of_faces = self.face_detector.detect_faces(image_path=image_path)
        if number_of_faces:
            logging.info("Faces detected")
        else:
            logging.info("Faces were not detected")


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
    alarm_system = AlarmSystem()
    alarm_system.activate()
