How to incorporate Strategy Patterns into the current existing implementation: 

The idea is to prevent the if else statements if there is a different parking strategy for each vehicle in the systme (also helps in Open - Close principle)

```py
# In a new file, e.g., strategies.py
from abc import ABC, abstractmethod

# This is the contract. Any class that inherits from this MUST provide a find_spot method.
class ParkingStrategy(ABC):
    
    @abstractmethod
    def find_spot(self, available_slots: dict) -> ParkingSlot | None:
        """
        Takes the dictionary of available spots and returns an available slot,
        or None if no suitable spot is found.
        """
        pass
```

```py
# Also in strategies.py

class BikeParkingStrategy(ParkingStrategy):
    def find_spot(self, available_slots: dict) -> ParkingSlot | None:
        # This is the logic SPECIFICALLY for bikes
        if len(available_slots[ParkingSlotType.SMALL]) > 0:
            return available_slots[ParkingSlotType.SMALL].pop(0)
        elif len(available_slots[ParkingSlotType.MEDIUM]) > 0:
            return available_slots[ParkingSlotType.MEDIUM].pop(0)
        elif len(available_slots[ParkingSlotType.LARGE]) > 0:
            return available_slots[ParkingSlotType.LARGE].pop(0)
        return None

class CarParkingStrategy(ParkingStrategy):
    def find_spot(self, available_slots: dict) -> ParkingSlot | None:
        # This is the logic SPECIFICALLY for cars
        if len(available_slots[ParkingSlotType.MEDIUM]) > 0:
            return available_slots[ParkingSlotType.MEDIUM].pop(0)
        elif len(available_slots[ParkingSlotType.LARGE]) > 0:
            return available_slots[ParkingSlotType.LARGE].pop(0)
        return None

# ... and you would create a TruckParkingStrategy as well
```


```py
# In your main file

# Import the new strategy classes
from strategies import BikeParkingStrategy, CarParkingStrategy, TruckParkingStrategy

class ParkingLot:
    def __init__(self, parking_slots: list[ParkingSlot], ticket_manager: TicketManager):
        # ... (all your existing setup code for slots) ...
        self.empty_parking_slots = {}
        self.parking_slots_initializer()

        # NEW: A dictionary that maps a vehicle type to its finding strategy object.
        # This is where you "register" your strategies.
        self.parking_strategies = {
            VehicleType.BIKE: BikeParkingStrategy(),
            VehicleType.CAR: CarParkingStrategy(),
            VehicleType.TRUCK: TruckParkingStrategy(), # Assuming you created this
        }

    # The OLD find_empty_slot method is completely DELETED from this class.

    def park_vehicle(self, vehicle: Vehicle, entry_time: int):
        # 1. Look up the correct strategy for the incoming vehicle.
        strategy = self.parking_strategies.get(vehicle.type)

        if not strategy:
            print(f"Error: No parking strategy defined for {vehicle.type}")
            return

        # 2. Delegate the task of finding a spot to the strategy object.
        #    The ParkingLot class doesn't care HOW it's found, only THAT it's found.
        print(f"Using {strategy.__class__.__name__} for vehicle {vehicle.reg_no}...")
        slot = strategy.find_spot(self.empty_parking_slots)

        if not slot:
            print("No empty slots for this vehicle type is possible")
            return

        # 3. The rest of your logic remains the same.
        slot.park_vehicle(vehicle)
        self.ticket_manager.new_ticket(vehicle, entry_time)
        self.parking_slot_filled[vehicle.reg_no] = slot
```