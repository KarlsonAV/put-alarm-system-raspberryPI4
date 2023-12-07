from camera import Camera

class AlarmSystem:
    def __init__(self) -> None:
        pass
    
    def take_photo(self, output_path: str):
        Camera.take_photo(output_path)

if __name__ == "__main__":
    alarm_system = AlarmSystem()
    alarm_system.take_photo("static/photos/test.jpeg")