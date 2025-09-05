from enum import Enum
import uuid


class VehicleType(Enum):
    BIKE = 1
    CAR = 2
    TRUCK = 3


class Vehicle:
    def __init__(self, reg_no: str, type: VehicleType):
        self.reg_no = reg_no
        self.type = type
        # print(f"New {self.type} INIT")


# parking slot now
class ParkingSlotType(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class ParkingSlot:
    def __init__(self, slot_no: int, slot_type: ParkingSlotType):
        self.slot_no = slot_no
        self.slot_type = slot_type
        self.vehicle = None

    def park_vehicle(self, vehicle: Vehicle):
        if self.vehicle:
            # not possible
            print("Already vehicle present")
            return False
        self.vehicle = vehicle
        print(
            f"{self.vehicle.type} - {self.vehicle.reg_no} parked at slot: {self.slot_no} \n"
        )

    def unpark_vehicle(self):
        self.vehicle = None
        print("Vehicle unparked \n")


# ticket manager part


class HourlyFare:
    BIKE = 10
    CAR = 20
    TRUCK = 30


class Ticket:
    def __init__(self, id: str, vehicle: Vehicle, entry_time: int):
        self.id = id
        self.vehicle = vehicle
        self.entry_time = entry_time  # entry time is hour number: 1, 2, 3 ..
        print(
            f"New ticket generated for Vehicle with: {self.vehicle.reg_no} at time: {self.entry_time}"
        )


class TicketPricer:
    def __init__(self):
        self.hourly_fare_dict_mapping = {
            VehicleType.BIKE: HourlyFare.BIKE,
            VehicleType.CAR: HourlyFare.CAR,
            VehicleType.TRUCK: HourlyFare.TRUCK,
        }

    def find_ticket_price(self, ticket: Ticket, current_hour: int):
        start_hour = ticket.entry_time
        hours_diff = current_hour - start_hour

        # based on hours diff, find price
        hourly_fare = self.hourly_fare_dict_mapping[ticket.vehicle.type]

        return hours_diff * hourly_fare


class TicketManager:
    # duty is to give a new ticket when a new vehicle is coming
    def __init__(self, ticket_pricer: TicketPricer):
        # for maintaining ticket ID to ticket; needed to resolve it
        self.ticket_mapping = {}
        self.ticket_pricer = ticket_pricer

    def new_ticket(self, vehicle: Vehicle, entry_time: int):
        ticket = Ticket(id=uuid.uuid4(), vehicle=vehicle, entry_time=entry_time)
        self.ticket_mapping[vehicle.reg_no] = ticket

    def resolve_ticket(self, vehicle: Vehicle):
        ticket = self.ticket_mapping.get(vehicle.reg_no, None)

        if not ticket:
            print("Ticket not found")

        # should find pricing for the particular ticket
        # assuming current hour is given by some other module
        price = self.ticket_pricer.find_ticket_price(ticket=ticket, current_hour=10)
        print(f"Vehicle {ticket.vehicle} needs to pay: {price} for the ticket")
        del self.ticket_mapping[vehicle.reg_no]
        print("Ticket resolved and deleted")


# main parking lot class


class ParkingLot:
    def __init__(self, parking_slots: list[ParkingSlot], ticket_manager: TicketManager):
        self.N = len(parking_slots)
        self.parking_slots = parking_slots
        self.ticket_manager = ticket_manager
        self.parking_slot_filled = {}
        print(f"Parking Lot with {self.N} slots initialized")

        # find free slots based on the parking slots array
        self.empty_parking_slots = {}
        self.parking_slots_initializer()

        # next types
        self.next_parking_types = {
            ParkingSlotType.SMALL: ParkingSlotType.MEDIUM,
            ParkingSlotType.MEDIUM: ParkingSlotType.LARGE,
        }

        self.parking_slots_type_mapping = {
            VehicleType.BIKE: ParkingSlotType.SMALL,
            VehicleType.CAR: ParkingSlotType.MEDIUM,
            VehicleType.TRUCK: ParkingSlotType.LARGE,
        }

    def parking_slots_initializer(self):
        for type in ParkingSlotType:
            self.empty_parking_slots[type] = []

        for slot in self.parking_slots:
            self.empty_parking_slots[slot.slot_type].append(slot)

        for type in self.empty_parking_slots:
            for slot in self.empty_parking_slots[type]:
                print(type, slot.slot_no)

    def find_empty_slot(self, vehicle: Vehicle):
        required_slot = self.parking_slots_type_mapping[vehicle.type]
        slots = self.empty_parking_slots[required_slot]
        if len(slots) == 0:
            while len(slots) == 0 and required_slot is not None:
                print(f"Finding {required_slot} slots")
                slots = self.empty_parking_slots[required_slot]
                required_slot = self.next_parking_types.get(required_slot, None)
            if len(slots) == 0:
                # not found
                return
            else:
                # slot found
                slot = slots.pop(0)
                return slot
        else:
            print("Direct type found")
            slot = slots.pop(0)
            return slot

    def park_vehicle(self, vehicle: Vehicle, entry_time: int):
        # see if a slot is present or not
        slot = self.find_empty_slot(vehicle)

        if not slot:
            print("No empty slots for this vehicle type is possible")
            return

        slot.park_vehicle(vehicle)

        # generate a new ticket of the user
        self.ticket_manager.new_ticket(vehicle, entry_time)

        self.parking_slot_filled[vehicle.reg_no] = slot

    def unpark_vehicle(self, vehicle: Vehicle):
        # see if present or not
        slot = self.parking_slot_filled.get(vehicle.reg_no)
        if not slot:
            print("Vehicle not present")
            return

        # resolve the ticket
        self.ticket_manager.resolve_ticket(vehicle)

        # add the slot back in the queue
        self.empty_parking_slots[slot.slot_type].append(slot)

        slot.unpark_vehicle()


if __name__ == "__main__":
    parking_slots = [
        ParkingSlot(1, ParkingSlotType.SMALL),
        ParkingSlot(2, ParkingSlotType.SMALL),
        ParkingSlot(3, ParkingSlotType.MEDIUM),
        ParkingSlot(4, ParkingSlotType.MEDIUM),
        ParkingSlot(5, ParkingSlotType.LARGE),
        ParkingSlot(6, ParkingSlotType.LARGE),
    ]

    ticket_manager = TicketManager(TicketPricer())
    parking_lot = ParkingLot(parking_slots, ticket_manager)

    # create vehicles
    v1 = Vehicle("123", VehicleType.BIKE)
    v2 = Vehicle("456", VehicleType.BIKE)
    v3 = Vehicle("789", VehicleType.CAR)
    v4 = Vehicle("7891", VehicleType.CAR)
    v5 = Vehicle("7892", VehicleType.CAR)
    v6 = Vehicle("78912", VehicleType.TRUCK)
    v7 = Vehicle("78922", VehicleType.TRUCK)

    # park vehicles
    print("\n--- Parking Vehicles ---")
    parking_lot.park_vehicle(v1, entry_time=1)  # entry at hour 1
    parking_lot.park_vehicle(v2, entry_time=2)  # entry at hour 2
    parking_lot.park_vehicle(v3, entry_time=3)  # entry at hour 3
    parking_lot.park_vehicle(v4, entry_time=3)  # entry at hour 3
    parking_lot.park_vehicle(v5, entry_time=3)  # entry at hour 3
    parking_lot.park_vehicle(v6, entry_time=3)
    parking_lot.park_vehicle(v7, entry_time=3)

    # unpark vehicles later
    print("\n--- Unparking Vehicles ---")
    parking_lot.unpark_vehicle(v1)  # should calculate fare
    parking_lot.unpark_vehicle(v2)
    parking_lot.unpark_vehicle(v3)

    parking_lot.park_vehicle(v3, entry_time=3)
