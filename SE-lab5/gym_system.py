"""Book fitness classes, manage their capacities and export class rosters."""

import json
from pathlib import Path

class_capacity = {"Yoga": 3, "HIIT": 2, "Spin": 4}
rosters = {}

def book_class(member_id, class_name, attendance_log=None):
    """Book one seat and optionally record the successful booking."""
    if class_name not in class_capacity:
        print("Unknown class:", class_name)
        return False
    roster = rosters.setdefault(class_name, [])
    if len(roster) >= class_capacity[class_name]:
        print("Class full:", class_name)
        return False
    roster.append(member_id)
    if attendance_log is not None:
        attendance_log.append(f"{member_id} -> {class_name}")
    return True

def cancel_booking(member_id, class_name):
    """Remove a booking if the member is on the class roster."""
    try:
        rosters[class_name].remove(member_id)
    except (KeyError, ValueError):
        print("Nothing to cancel")

def set_capacity(class_name, seats):
    """Set a nonnegative integer capacity that covers existing bookings."""
    valid_integer = isinstance(seats, int) and not isinstance(seats, bool)
    if not valid_integer or seats < len(rosters.get(class_name, [])):
        print("Invalid capacity:", seats)
        return
    class_capacity[class_name] = seats

def add_members(class_name, count):
    """Book walk-in guests until the requested count or capacity is reached."""
    for index in range(count):
        if not book_class(f"GUEST-{index}", class_name):
            break

def export_roster(file="gym_schedule.json"):
    """Write the current rosters to a UTF-8 JSON file."""
    with open(file, "w", encoding="utf-8") as schedule:
        json.dump(rosters, schedule)

def clear_old_exports(prefix="old_"):
    """Remove local JSON exports whose filenames start with a literal prefix."""
    if not prefix:
        raise ValueError("An export prefix is required")
    for entry in Path.cwd().iterdir():
        if entry.name.startswith(prefix) and entry.name.endswith(".json"):
            if entry.is_file() or entry.is_symlink():
                entry.unlink(missing_ok=True)

def show_rosters():
    """Print each class and the members attending it."""
    for class_name, members in rosters.items():
        print(class_name, ":", ", ".join(map(str, members)))

def main():
    """Run a sample booking session and export the resulting schedule."""
    book_class("M1", "Yoga")
    book_class("M2", "Yoga")
    book_class("M3", "Yoga")
    book_class("M4", "Yoga")
    book_class(55, "HIIT")
    book_class("M5", "Pilates")
    set_capacity("Spin", -2)
    add_members("Spin", 3)
    cancel_booking("M9", "Boxing")
    answer = input("How many walk-in guests for HIIT? (Enter for 1): ")
    try:
        count = int(answer.strip() or "1")
        if count < 0:
            raise ValueError
    except ValueError:
        print("Please enter a nonnegative whole number. Skipping walk-ins.")
    else:
        add_members("HIIT", count)
    clear_old_exports()
    export_roster()
    show_rosters()

if __name__ == "__main__":
    main()
