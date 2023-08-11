import csv
from datetime import datetime, timedelta

wgu_address = "4001 S 700 E"

"""
    TABLES
"""
hash_table = [[], [], [], [], [], [], [], [], [], []]
distances_table = []


"""
    FUNCTIONS
"""

def hash_function(package_id):
    return int(package_id) % 10


def insert_package(package):
    index = hash_function(package.package_id)
    hash_table[index].append(package)


def get_row_number(address):
    with open("addresses.csv", 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if row[0] == address:
                return i
    return None


def get_distance(address1, address2):
    row1 = get_row_number(address1)
    row2 = get_row_number(address2)
    return distances_table[row1][row2]


"""
    CLASSES
"""


class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.status = status


class Truck:


    def __init__(self):
        self.packages = []
        self.delivery_times = []

    def add_package_by_id(self, package_id):
        index = hash_function(package_id)
        for package in hash_table[
            index]:
            if package.package_id == package_id:
                self.packages.append(package)
                return True
        return False


    def sort_packages_by_distance(self, wgu_address):
        sorted_packages = []
        unsorted_packages = self.packages.copy()

        def get_distance_from_wgu(package):
            return get_distance(wgu_address, package.address)

        furthest_package = max(unsorted_packages, key=get_distance_from_wgu)

        sorted_packages.append(furthest_package)
        unsorted_packages.remove(furthest_package)

        current_address = furthest_package.address

        while unsorted_packages:
            def get_distance_from_current(package):
                return get_distance(current_address, package.address)

            nearest_package = min(unsorted_packages, key=get_distance_from_current)
            sorted_packages.append(nearest_package)
            unsorted_packages.remove(nearest_package)
            current_address = nearest_package.address

        self.packages = sorted_packages

    def generate_delivery_times(self, start_time, wgu_address):
        delivery_times = []
        current_time = start_time
        last_address = wgu_address

        for package in self.packages:
            distance = get_distance(last_address, package.address)
            travel_time_seconds = distance / 18 * 3600
            current_time += timedelta(seconds=travel_time_seconds)
            delivery_times.append(current_time)
            last_address = package.address

        distance_to_wgu = get_distance(last_address, wgu_address)
        travel_time_to_wgu_seconds = distance_to_wgu / 18 * 3600
        current_time += timedelta(seconds=travel_time_to_wgu_seconds)
        delivery_times.append(current_time)

        self.delivery_times = delivery_times

    def update_delivery_status(self, current_time):
        start_time = datetime.strptime("08:00 AM", "%I:%M %p")
        if self == truck3:
            start_time = truck1.delivery_times[-1]

        for package, delivery_time in zip(self.packages, self.delivery_times):
            if current_time < start_time:
                package.delivery_status = "At The Hub"
            elif delivery_time <= current_time:
                package.delivery_status = "Delivered"
            else:
                package.delivery_status = "En Route"

    def calculate_distance(self, time):
        if self is truck3:
            if time < truck1.delivery_times[-1]:
                return 0
            elif time > self.delivery_times[-1]:
                elapsed_hours = (self.delivery_times[-1] - truck1.delivery_times[-1]).seconds / 3600
                return 18 * elapsed_hours
            else:
                elapsed_hours = (time - truck1.delivery_times[-1]).seconds / 3600
                return 18 * elapsed_hours
        else:
            base_time = datetime.strptime("08:00 AM", "%I:%M %p")
            if time < base_time:
                return 0
            elif time > self.delivery_times[-1]:
                elapsed_hours = (self.delivery_times[-1] - base_time).seconds / 3600
                return 18 * elapsed_hours
            else:
                elapsed_hours = (time - base_time).seconds / 3600
                return 18 * elapsed_hours


'''''
    POPULATION OF TABLES/CREATION OF PACKAGE OBJECTS
'''''

with open("distances.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        row_data = [float(value) for value in row]
        distances_table.append(row_data)

with open("packages.csv", 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        package_id, address, city, state, zip_code, deadline, weight, status = row
        package = Package(int(package_id), address, city, state, zip_code, deadline, weight, status)
        insert_package(package)


"""
    CREATION OF TRUCK OBJECTS
"""

truck1 = Truck()
truck2 = Truck()
truck3 = Truck()

"""
    TRUCK PACKAGE LOADING/SORTING
"""
truck1.add_package_by_id(1)
truck1.add_package_by_id(4)
truck1.add_package_by_id(40)
truck1.add_package_by_id(13)
truck1.add_package_by_id(14)
truck1.add_package_by_id(15)
truck1.add_package_by_id(19)
truck1.add_package_by_id(16)
truck1.add_package_by_id(20)
truck1.add_package_by_id(21)
truck1.add_package_by_id(27)
truck1.add_package_by_id(31)
truck1.add_package_by_id(35)
truck1.add_package_by_id(39)
truck1.add_package_by_id(12)

truck2.add_package_by_id(2)
truck2.add_package_by_id(3)
truck2.add_package_by_id(5)
truck2.add_package_by_id(7)
truck2.add_package_by_id(8)
truck2.add_package_by_id(10)
truck2.add_package_by_id(11)
truck2.add_package_by_id(17)
truck2.add_package_by_id(18)
truck2.add_package_by_id(22)
truck2.add_package_by_id(23)
truck2.add_package_by_id(24)
truck2.add_package_by_id(26)
truck2.add_package_by_id(29)
truck2.add_package_by_id(36)
truck2.add_package_by_id(38)

truck3.add_package_by_id(6)
truck3.add_package_by_id(9)
truck3.add_package_by_id(25)
truck3.add_package_by_id(28)
truck3.add_package_by_id(30)
truck3.add_package_by_id(32)
truck3.add_package_by_id(33)
truck3.add_package_by_id(34)
truck3.add_package_by_id(37)

truck1.sort_packages_by_distance(wgu_address)
truck2.sort_packages_by_distance(wgu_address)
truck3.sort_packages_by_distance(wgu_address)

"""
    TRUCK DELIVERY TIME GENERATION
"""
truck1.generate_delivery_times(datetime.strptime("8:00 AM", "%I:%M %p"), wgu_address)
truck2.generate_delivery_times(datetime.strptime("8:00 AM", "%I:%M %p"), wgu_address)
truck3.generate_delivery_times(truck1.delivery_times[-1], wgu_address)

"""
    UI
"""
print("*** ROUTING PROGRAM ***")

while True:
    user_input_time = input("Enter a time (Including AM or PM): ")

    try:
        user_input_time = datetime.strptime(user_input_time, "%I:%M %p")
        break
    except ValueError:
        print("Invalid format. Please enter the time in the format Hour:Minute AM/PM")

print("--------------------- \n      TRUCK 1:\n---------------------")
truck1.update_delivery_status(user_input_time)

for package in truck1.packages:
    print("Package ", package.package_id, ": ", package.delivery_status, sep="")

distance1 = truck1.calculate_distance(user_input_time)
print("\nDistance traveled:", distance1, "miles\n")
print("--------------------- \n      TRUCK 2:\n---------------------")
truck2.update_delivery_status(user_input_time)

for package in truck2.packages:
    print("Package ", package.package_id, ": ", package.delivery_status, sep="")
distance2 = truck2.calculate_distance(user_input_time)
print("\nDistance traveled:", distance2, "miles\n")

print("--------------------- \n      TRUCK 3:\n---------------------")
truck3.update_delivery_status(user_input_time)

for package in truck3.packages:
    print("Package ", package.package_id, ": ", package.delivery_status, sep="")

distance3 = truck3.calculate_distance(user_input_time)
print("\nDistance traveled:", distance3, "miles\n")

if user_input_time >= truck3.delivery_times[-1]:
    print("--------------------- \n END OF DAY REPORT:\n---------------------")
    print("Miles Driven:", distance1 + distance2 + distance3)
    print("End of Day:", truck3.delivery_times[-1].strftime("%I:%M %p"))
