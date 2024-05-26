# parking_status_service.py
from parking_spot_observer import ParkingSpotObserver

class ParkingStatusService(ParkingSpotObserver):
    def __init__(self):
        self.parking_status = {}
    
    def update(self, statuses):
        self.parking_status = statuses
        self.display_status()
    
    def display_status(self):
        print("Current Parking Status:")
        for spot_id, status in self.parking_status.items():
            print(f"Spot {spot_id}: {status}")
