# parking_spot_observer.py
from abc import ABC, abstractmethod

class ParkingSpotObserver(ABC):
    @abstractmethod
    def update(self, statuses):
        pass
