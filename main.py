# main.py
from parking_spot_subject import ParkingSpotSubject
from parking_status_service import ParkingStatusService
from web_notification_service import WebNotificationService
from parking_spot_detector import ParkingSpotDetector

if __name__ == '__main__':
    subject = ParkingSpotSubject()
    
    status_service = ParkingStatusService()
    web_service = WebNotificationService()
    
    subject.register_observer(status_service)
    subject.register_observer(web_service)
    
    # Start the web server for notifications
    web_service.send_notification()
    
    # Initialize and start the parking spot detector
    video_file = 'video.mp4'  # Path to the uploaded video file
    detector = ParkingSpotDetector(subject=subject, video_file=video_file)
    detector.detect_parking_spot()
