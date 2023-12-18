import os
import logging

logging.getLogger().setLevel(logging.INFO)


class Camera:
    @staticmethod
    def take_photo(output_path: str) -> str:
        try:
            logging.info("Taking photo")
            os.system(f"libcamera-still  -o {output_path} -n -t 0.01")
            logging.info("Photo captured")
            return output_path
        except Exception as e:
            logging.error(f"Error: {e}\nCouldn't save photo {output_path}")
        
        return ""
            
