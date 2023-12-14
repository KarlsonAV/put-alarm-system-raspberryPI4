import RPi.GPIO as GPIO
from typing import Callable

class MotionSensor:
    def __init__(self, pin: int) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)
        self.pin = pin
        
    def detect_motion(self, motion_detected_callback: Callable) -> None:
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=motion_detected_callback, bouncetime=200)
