import cv2
import imutils

class FaceDetector:
    def __init__(self, detector_path: str) -> None:
        self.face_detector = cv2.CascadeClassifier(detector_path)

    def detect_faces(self, image_path: str) -> int:
        # Read image		
        img = cv2.imread(image_path)
        
        # Resize image
        img = imutils.resize(img, width=min(400, img.shape[1]))
        
        # Convert into RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # Detect faces
        faces = self.face_detector.detectMultiScale(gray, 1.1, 3)
        
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        number_of_detected_faces = len(faces)
        cv2.imwrite(image_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        
        return number_of_detected_faces