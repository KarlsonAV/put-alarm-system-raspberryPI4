import os
import logging
import time
import concurrent.futures
import sqlite3

from datetime import datetime

from camera import Camera
from motion_sensor import MotionSensor
from sound_sensor import SoundSensor
from face_detector import FaceDetector
from email_sender import EmailSender


logging.getLogger().setLevel(logging.INFO)

PIN_MOTION_SENSOR = 23
PIN_SOUND_SENSOR = 24
FACE_DETECTOR_PATH = "haarcascades/haarcascade_frontalface_default.xml"
MAX_THREADS_WORKERS = 5
DATABASE_PATH = "report_database.db"
SMTP_SERVER = 'smtp-relay.brevo.com'
SMTP_PORT = 587
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')


class AlarmSystem:
    def __init__(self) -> None:
        self.motion_sensor = MotionSensor(pin=PIN_MOTION_SENSOR)
        self.sound_sensor = SoundSensor(pin=PIN_SOUND_SENSOR)
        self.face_detector = FaceDetector(FACE_DETECTOR_PATH)
        self.email_sender = EmailSender(
            smtp_server=SMTP_SERVER,
            smtp_port=SMTP_PORT,
            sender_email=SENDER_EMAIL,
            sender_password=SENDER_PASSWORD
        )
        self.sound_detection_count = 0
        self.last_sound_detection_time = 0
        self.status = 0


    def send_email(self, image_path: str, num_faces: int, date_time: str) -> None:
        email_subject = f"[ALARM SYSTEM] Motion Detected {date_time}"
        email_body = f"Alarm system detected motion. Number of Faces Detected: {num_faces}"
        logging.info("Sending email")
        self.email_sender.send_email_with_photo(
            recipient_email=RECIPIENT_EMAIL,
            subject = email_subject,
            body = email_body,
            photo_path=image_path
        )


    def add_report(self, image_path: str, num_faces: int, date: str) -> None:
        try:
            with open(image_path, 'rb') as image_file:
                image_blob = image_file.read()
                
            connection = sqlite3.connect(DATABASE_PATH)
            cursor = connection.cursor()

            cursor.execute('''
                INSERT INTO alarm_system (DATE, image, Faces) VALUES (?, ?, ?)
            ''', (date, image_blob, num_faces))

            connection.commit()
            connection.close()

            logging.info("Report added to the database.")
        
        except Exception as e:
            logging.error(f"Error adding report to the database: {str(e)}")


    def _process_motion_detection(self):
        current_datetime = datetime.now()
        image_path = os.path.join("static", "photos", '_'.join(str(current_datetime).split(' ')))
        image_path += ".jpeg"
        image_path = self.take_photo(output_path=image_path)
        if image_path:
            num_faces = self.detect_faces(image_path=image_path)
            self.add_report(image_path, num_faces, str(current_datetime))
            self.send_email(image_path, num_faces, str(current_datetime))
            os.remove(image_path)
    
    
    def _motion_detected(self, channel: int) -> None:
        if not self.status:
            return
        
        logging.info(f"Motion Detected [{datetime.now()}]")
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS_WORKERS) as executor:
            executor.submit(self._process_motion_detection)


    def _sound_detected(self, channel: int) -> None:
        current_time = time.time()
        logging.info(f"Sound Detected [{datetime.now()}]")

        if current_time - self.last_sound_detection_time > 0.5:
            # Reset the count if more than half second has passed since the last detection
            self.sound_detection_count = 0

        self.sound_detection_count += 1
        self.last_sound_detection_time = current_time

        if self.sound_detection_count == 3:
            logging.info("Three consecutive sound detections within 0.5 second.")
            self.disable()

        elif self.sound_detection_count == 2:
            logging.info("Two consecutive sound detections within 0.5 second.")
            if self.status == 1:
                self.deactivate()
            else:
                self.activate()
                

    def take_photo(self, output_path: str) -> None:
        return Camera.take_photo(output_path)


    def detect_faces(self, image_path: str) -> int:
        logging.info("Face detection activated")
        number_of_faces = self.face_detector.detect_faces(image_path=image_path)
        if number_of_faces:
            logging.info("Faces detected")
        else:
            logging.info("Faces were not detected")
        
        return number_of_faces


    def run(self) -> None:
        self.enable()
        try:
            self.motion_sensor.detect_motion(motion_detected_callback=self._motion_detected)
            self.sound_sensor.detect_sound(sound_detected_callback=self._sound_detected)

            while self.status >= 0:
                pass

        except KeyboardInterrupt:
            logging.info("Ctrl+C pressed. Stopping the alarm system.")
            self.deactivate()


    def deactivate(self) -> None:
        self.status = 0
        logging.info("Alarm system is deactivated")

        
    def activate(self) -> None:
        self.status = 1
        logging.info("Alarm system is activated")


    def enable(self) -> None:
        logging.info("Alarm system begins to run...")
        self.activate()

        
    def disable(self) -> None:
        self.status = -1
        logging.info("Alarm system stops to run...")
    

if __name__ == "__main__":
    alarm_system = AlarmSystem()
    alarm_system.run()
