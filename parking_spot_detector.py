# parking_spot_detector.py
import cv2
import numpy as np
import time
import json
from parking_spot_subject import ParkingSpotSubject

# Define parking slots in column-major order with the specified empty spaces
parking_slots = [
    # Column 1
    (55, 100),   # 1
    (56, 146),   # 2
    (51, 192),   # 3
    (51, 241),   # 4
    (53, 290),   # 5
    (55, 337),   # 6
    (55, 385),   # 7
    (52, 431),   # 8
    (53, 479),   # 9
    (52, 527),   # 10
    (51, 573),   # 11
    (51, 625),   # 12

    # Column 2
    (163, 99),   # 13
    (164, 147),  # 14
    (158, 194),  # 15
    (159, 243),  # 16
    (161, 290),  # 17
    (162, 339),  # 18
    (160, 388),  # 19
    (162, 429),  # 20
    (162, 479),  # 21
    (168, 525),  # 22
    (165, 576),  # 23
    (165, 620),  # 24

    # Column 3
    (405, 90),   # 25
    (402, 138),  # 26
    (405, 189),  # 27
    (402, 239),  # 28
    (402, 289),  # 29
    (402, 338),  # 30
    (404, 382),  # 31
    (405, 427),  # 32
    # Empty space here
    (405, 526),  # 33
    (403, 569),  # 34
    (406, 619),  # 35

    # Column 4
    (514, 92),   # 36
    (511, 139),  # 37
    (514, 187),  # 38
    (512, 236),  # 39
    (513, 284),  # 40
    (513, 329),  # 41
    (511, 380),  # 42
    (511, 426),  # 43
    (512, 524),  # 44
    # Empty space here
    (512, 568),  # 45
    (513, 620),  # 46

    # Column 5
    (751, 88),   # 47
    (751, 136),  # 48
    (750, 188),  # 49
    (753, 232),  # 50
    (753, 276),  # 51
    (751, 327),  # 52
    (750, 380),  # 53
    (757, 427),  # 54
    (755, 480),  # 55
    (757, 518),  # 56
    (760, 573),  # 57
    (760, 616),  # 58

    # Column 6
    # Empty space in the first row
    (892, 150),  # 59
    (892, 190),  # 60
    (893, 235),  # 61
    (894, 284),  # 62
    (897, 330),  # 63
    (898, 375),  # 64
    (901, 424),  # 65
    (903, 474),  # 66
    (903, 520),  # 67
    (901, 576),  # 68
    (901, 620),  # 69
]

rect_width, rect_height = 100, 33
threshold = 30

class ParkingSpotDetector:
    def __init__(self, subject, video_file):
        self.subject = subject
        self.video_file = video_file
        self.last_call_time = time.time()
        self.prevFreeslots = 0
    
    def convert_grayscale(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_image = frame.copy()
        contour_image[:] = 0
        cv2.drawContours(contour_image, contours, -1, (255, 255, 255), thickness=2)
        return contour_image

    def mark_slots(self, frame, grayscale_frame):
        current_time = time.time()
        freeslots = 0
        slot_statuses = {}

        for idx, (x, y) in enumerate(parking_slots):
            spot_id = f"{idx + 1}"  # Sequential numbering from 1
            x1 = x + 10
            x2 = x + rect_width - 11
            y1 = y + 4
            y2 = y + rect_height
            crop = grayscale_frame[y1:y2, x1:x2]
            gray_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            count = cv2.countNonZero(gray_crop)
            color, thick = [(0, 255, 0), 5] if count < threshold else [(0, 0, 255), 2]
            status = "available" if count < threshold else "occupied"
            if count < threshold:
                freeslots += 1

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thick)
            cv2.putText(frame, spot_id, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            slot_statuses[spot_id] = status

        if current_time - self.last_call_time >= 0.1:
            self.last_call_time = current_time
            self.prevFreeslots = freeslots
        
        self.subject.set_status(slot_statuses)
        return frame
    
    def detect_parking_spot(self):
        cap = cv2.VideoCapture(self.video_file)
        if not cap.isOpened():
            print("Error: Could not open video file.")
            return
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            grayscale_frame = self.convert_grayscale(frame)
            out_image = self.mark_slots(frame, grayscale_frame)

            # Save the status to a JSON file
            with open('static/status.json', 'w') as f:
                json.dump(self.subject.get_status(), f)
            
            # Save the final frame as an image
            cv2.imwrite('static/output_frame.jpg', out_image)
            
            # Display the result (for debugging purposes)
            cv2.imshow("Parking Spot Detector", out_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    video_file = 'video.mp4'  # Path to the uploaded video file
    subject = ParkingSpotSubject()
    detector = ParkingSpotDetector(subject=subject, video_file=video_file)
    detector.detect_parking_spot()
