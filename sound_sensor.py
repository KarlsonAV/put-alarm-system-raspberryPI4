import RPi.GPIO as GPIO
from typing import Callable

class SoundSensor:
    def __init__(self, pin: int) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)
        self.pin = pin
        
    def detect_sound(self, sound_detected_callback: Callable) -> None:
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=sound_detected_callback, bouncetime=200)
