"""
The parking lot has multiple parking spots.
Each parking spot can hold one vehicle.
Vehicles can be of type Car or Bike (for now).

System should allow:
    Park a vehicle (assign a spot if available).
    Remove a vehicle (free the spot).
    Check availability of spots.
"""

import time

###### vehicles 

class Vehicle: 
    def __init__(self, reg):
        self.reg = reg
        self.entry_time = time.time()
        self.exit_time = None 

        print(f"Vehicle entered at {self.entry_time}")


class Bike(Vehicle): 
    def __init__(self, *args, **kwargs):
        print("Bike entered")
        super().__init__(*args, **kwargs)


###### parking slot

class ParkingSlot:
    def __init__(self, slot_id):
        self.slot_id = slot_id
        self.vehicle = None

    # put a vehicle in a parking slot
    def park_vehicle(self, vehicle): 
        if self.vehicle: 
            print("Vehicle already present, cannot park again")
            return False
        print(f"Parking vehicle {vehicle} at {self.slot_id}")
        self.vehicle = vehicle
        return True

    def unpark_vehicle(self): 
        # return vehicle
        if not self.vehicle:
            print("no vehicle present")
            return None
        print(f"unparked vehicle from {self.slot_id}")
        v = self.vehicle
        self.vehicle = None
        return v


####### parking lot
class ParkingLot:
    def __init__(self, N):
        self.N = N
        print(f"init with {N} parking slots")

        self.parking_slots_mapping = {}
        self.all_parking_slots = [ParkingSlot(i) for i in range(N)]

    def find_remaining_capacity(self): 
        return self.N - len(self.parking_slots_mapping.keys())

    def find_parking_slot(self): 
        for i in range(0, self.N):
            if i not in self.parking_slots_mapping:
                return i
        return None

    def park_vehicle(self, vehicle: Vehicle): 
        slot_id = self.find_parking_slot()
        if slot_id is None:   # better than `if not slot` since slot=0 is valid
            print("cannot park, full")
            return False
    
        slot_obj = self.all_parking_slots[slot_id]
        is_parked = slot_obj.park_vehicle(vehicle)
        if is_parked:
            self.parking_slots_mapping[slot_id] = slot_obj
            return True
    
        return False


    def unpark_vehicle(self, reg): 
        for slot_id, slot in list(self.parking_slots_mapping.items()):
            if slot.vehicle and slot.vehicle.reg == reg:
                slot.unpark_vehicle()
                del self.parking_slots_mapping[slot_id]
                return True
        print("Vehicle not found")

    def print_all_vehicles(self): 
        for slot_id, slot in self.parking_slots_mapping.items():
            print(f"{slot_id}: {slot.vehicle}")


if __name__ == "__main__":
    parking_lot = ParkingLot(5)

    bike1 = Bike("123")
    car1 = Bike("456")

    parking_lot.park_vehicle(bike1)
    parking_lot.park_vehicle(car1)

    parking_lot.print_all_vehicles()

    parking_lot.unpark_vehicle("123")

    print("Remaining capacity:", parking_lot.find_remaining_capacity())
    parking_lot.print_all_vehicles()


