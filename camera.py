import os


class Camera:

    @staticmethod
    def take_photo(output_path: str) -> str:
        output = ""
        try:
            os.system(f"libcamera-still  -o {output_path} -n -t 0.01")
            output = f"Successfully saved photo {output_path}"
        except Exception as e:
            output = f"Error: {e}\nCouldn't save photo {output_path}"
            
        return output
            
