import json
import os
from typing import List, Dict, Optional
print("*****SAI RAM MEN'S PG*****")
DATA_FILE = "rooms.json"

def load_data(path: str = DATA_FILE) -> List[Dict]:
    """Load rooms list from JSON file. If file not exists, return empty list."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:

            print("Warning: JSON file corrupted. Starting with empty data.")
            return []
        
def save_data(rooms: List[Dict], path: str = DATA_FILE) -> None:
    """Save rooms list to JSON file (pretty printed)."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rooms, f, indent=2, ensure_ascii=False)
        
def create_room(floor: int, room_number: str, sharing: int) -> Dict:
    """Create a new room dictionary. occupants is a list of tenant dicts."""
    if sharing < 1 or sharing > 5:
        raise ValueError("sharing must be between 1 and 5")
    return {
        "floor": floor,
        "room_number": room_number,
        "sharing": sharing,
        "capacity": sharing,
        "occupants": []  # each occupant: {"name":..., "age":..., "phone":...}
    }

def add_room(rooms: List[Dict], floor: int, room_number: str, sharing: int) -> None:
    """Add room if not duplicate."""
    for r in rooms:
        if r["floor"] == floor and r["room_number"] == room_number:
            print("Room already exists — not added.")
            return
    rooms.append(create_room(floor, room_number, sharing))
    print("Room added.")

def find_available_rooms(rooms: List[Dict], sharing: Optional[int] = None) -> List[Dict]:
    """Return rooms that are not full. Optionally filter by sharing (1-5)."""
    available = []
    for r in rooms:
        if len(r["occupants"]) < r["capacity"]:
            if sharing is None or r["sharing"] == sharing:
                available.append(r)
    return available

def pretty_print_room(r: Dict) -> None:
    """Print one room nicely with occupant details."""
    print(f"Floor: {r['floor']}, Room: {r['room_number']}, Sharing: {r['sharing']} "
          f"(capacity {r['capacity']}), Occupied: {len(r['occupants'])}")
    if r['occupants']:
        for i, o in enumerate(r['occupants'], 1):
            print(f"  {i}. {o['name']} (age: {o['age']}, phone: {o['phone']})")

def list_all_rooms(rooms: List[Dict]) -> None:
    """Show all rooms with occupants."""
    if not rooms:
        print("No rooms in database.")
        return
    for r in sorted(rooms, key=lambda x: (x["floor"], x["room_number"])):
        pretty_print_room(r)

def rent_room(rooms: List[Dict], floor: int, room_number: str,
              name: str, age: int, phone: str) -> bool:
    """Add a tenant to a room if space available. Returns True on success."""
    for r in rooms:
        if r["floor"] == floor and r["room_number"] == room_number:
            if len(r["occupants"]) < r["capacity"]:
            
                if any(o["name"].lower() == name.lower() for o in r["occupants"]):
                    print("Tenant with this name already in the room.")
                    return False
                occupant = {"name": name, "age": age, "phone": phone}
                r["occupants"].append(occupant)
                print(f"{name} assigned to room {room_number} on floor {floor}.")
                return True
            else:
                print("Room is full.")
                return False
    print("Room not found.")
    return False

def vacate_tenant(rooms: List[Dict], floor: int, room_number: str, name: str) -> bool:
    """Remove tenant by name from specified room. Return True if removed."""
    for r in rooms:
        if r["floor"] == floor and r["room_number"] == room_number:
            for i, o in enumerate(r["occupants"]):
                if o["name"].lower() == name.lower():
                    r["occupants"].pop(i)
                    print(f"{name} removed from room {room_number} on floor {floor}.")
                    return True
            print("Tenant not found in that room.")
            return False
    print("Room not found.")
    return False

def remove_room(rooms: List[Dict], floor: int, room_number: str) -> bool:
    """Remove an empty room. Return True if removed."""
    for i, r in enumerate(rooms):
        if r["floor"] == floor and r["room_number"] == room_number:
            if len(r["occupants"]) > 0:
                print("Cannot remove room — occupants present.")
                return False
            rooms.pop(i)
            print("Room removed.")
            return True
    print("Room not found.")
    return False

def prompt_int(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    """Prompt user for integer with optional min/max checks."""
    while True:
        v = input(prompt).strip()
        if not v:
            print("Please enter a value.")
            continue
        if not v.isdigit():
            print("Enter a valid integer.")
            continue
        iv = int(v)
        if (min_val is not None and iv < min_val) or (max_val is not None and iv > max_val):
            print(f"Enter a value between {min_val} and {max_val}.")
            continue
        return iv

def prompt_phone(prompt: str) -> str:
    """Very simple phone validation: digits only and length 7-15."""
    while True:
        p = input(prompt).strip()
        if not p.isdigit() or not (7 <= len(p) <= 15):
            print("Enter digits only (7-15 digits).")
            continue
        return p

def menu():
    rooms = load_data()
    while True:
        print("\nHostel Manager — Options")
        print("1)ADD ROOM\n2)LIST OF ALL ROOMS\n3)LIST OF AVAILABLE ROOMS\n4)RENT ROOM TO A TENANT\n5)REMOVE TENANT FROM ROOM\n6)REMOVE ROOM\n7)SAVE\n8)EXIt")         
        choice = input("Choose option: ").strip()

        if choice == "1":
            floor = prompt_int("Floor (1-6): ", 1, 6)
            room_number = input("Room number (e.g. 601A): ").strip()
            sharing = prompt_int("Sharing (1-5): ", 1, 5)
            add_room(rooms, floor, room_number, sharing)

        elif choice == "2":
            list_all_rooms(rooms)

        elif choice == "3":
            s = input("Enter sharing to filter (1-5) or press Enter for all: ").strip()
            if s == "":
                avail = find_available_rooms(rooms)
            else:
                if not s.isdigit() or not (1 <= int(s) <= 5):
                    print("Invalid sharing. Showing all available.")
                    avail = find_available_rooms(rooms)
                else:
                    avail = find_available_rooms(rooms, int(s))
            if not avail:
                print("No available rooms found.")
            else:
                print(f"{len(avail)} available room(s):")
                for r in avail:
                    pretty_print_room(r)

        elif choice == "4":
            floor = prompt_int("Floor (1-6): ", 1, 6)
            room_number = input("Room number: ").strip()
            name = input("Tenant name: ").strip()
            if not name:
                print("Name required.")
                continue
            age = prompt_int("Age: ", 1, 120)
            phone = prompt_phone("Phone (digits only): ")
            rent_room(rooms, floor, room_number, name, age, phone)

        elif choice == "5":
            floor = prompt_int("Floor (1-6): ", 1, 6)
            room_number = input("Room number: ").strip()
            name = input("Remove tenant by name: ").strip()
            if not name:
                print("Name required.")
                continue
            vacate_tenant(rooms, floor, room_number, name)

        elif choice == "6":
            floor = prompt_int("Floor (1-6): ", 1, 6)
            room_number = input("Room number: ").strip()
            remove_room(rooms, floor, room_number)

        elif choice == "7":
            save_data(rooms)
            print("Saved to", DATA_FILE)

        elif choice == "8":
            save_data(rooms)
            print("Saved. Exiting.")
            break

        else:
            print("Invalid  Try again.")


if __name__== "__main__":
    menu()
