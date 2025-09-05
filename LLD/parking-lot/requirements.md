# Parking Lot System Requirements

## Functional Requirements 📋

These are the core features the system must have.

### 1. Support for Different Vehicle and Spot Types
* **Layman's Explanation:** A parking lot isn't a one-size-fits-all place. The system needs to understand different vehicle sizes and match them to appropriate spots.
* **Example:**
    * **Vehicles to support:** `Bike`, `Car`, `Truck`.
    * **Parking spots to support:** `Small`, `Medium`, `Large`.
    * **The Rules:**
        * A `Bike` can park in a `Small`, `Medium`, or `Large` spot.
        * A `Car` can park in a `Medium` or `Large` spot.
        * A `Truck` can only park in a `Large` spot.

---

### 2. Parking a Vehicle and Issuing a Ticket
* **Layman's Explanation:** When a vehicle enters, the system must find a suitable empty spot. If it finds one, it should occupy the spot and give the driver a virtual **ticket** containing all important information. If no spot is available, it should turn the vehicle away.
* **Example:**
    * A `Car` with registration number "KA-01-HH-1234" arrives.
    * The system first looks for an available `Medium` spot. If none are found, it then looks for an available `Large` spot.
    * It finds an available `Medium` spot with ID "M-05".
    * The system generates a **Ticket** that links the car's registration number, the spot ID, and the exact time of entry.

---

### 3. Unparking a Vehicle and Freeing the Spot
* **Layman's Explanation:** When the driver is ready to leave, they use their ticket to "check out." The system uses the ticket to find which vehicle is leaving and from which spot. Afterward, the spot must be marked as empty again for the next person.
* **Example:**
    * The driver with the ticket from the previous example wants to leave.
    * The system finds that vehicle "KA-01-HH-1234" is in spot "M-05".
    * It marks spot "M-05" as available again.

---

### 4. Fee Calculation
* **Layman's Explanation:** The system needs to calculate the parking cost based on the duration. The price per hour can be different for different vehicle types.
* **Example:**
    * **Hourly Rates:**
        * `Bike`: ₹10 per hour.
        * `Car`: ₹20 per hour.
        * `Truck`: ₹30 per hour.
    * If a `Car` was parked for 2 hours, the total fee would be 2 * ₹20 = ₹40.
    * Billing is for every full hour started (e.g., 1 hour and 5 minutes is billed as 2 hours).

---

### 5. Parking Lot Status Display
* **Layman's Explanation:** The system must be able to show real-time availability on a display board at the entrance.
* **Example:**
    * `Small Spots Free: 5`
    * `Medium Spots Free: 0`
    * `Large Spots Free: 2`

***

## Non-Functional Requirements ⚙️

These requirements define the quality and design of the system.

* **Extensibility:** The code should be designed so that adding a new vehicle type (e.g., `ElectricCar`) or a new spot type (e.g., `ElectricChargingSpot`) doesn't require rewriting the entire system.
* **Readability:** The code should be clean, well-structured, and easy for another developer to understand.