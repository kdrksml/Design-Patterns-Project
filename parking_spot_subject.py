# parking_spot_subject.py
class ParkingSpotSubject:
    def __init__(self):
        self.observers = []
        self.statuses = {}
    
    def register_observer(self, observer):
        self.observers.append(observer)
    
    def remove_observer(self, observer):
        self.observers.remove(observer)
    
    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.statuses)
    
    def set_status(self, statuses):
        self.statuses = statuses
        self.notify_observers()
    
    def get_status(self):
        return self.statuses
