import os


class Camera:

    @staticmethod
    def take_photo(output_path: str) -> str:
        os.system(f"libcamera-still -o {output_path}")
