import csv
from datetime import datetime, timedelta

wgu_address = "4001 S 700 E"

"""
    TABLE
"""
distances_table = []

"""
    FUNCTIONS
"""


def lookup(package_id):
    for truck in truck_list:
        for i, package in enumerate(truck.packages):
            if package_id == package.package_id:
                print("--------------------- \n      PACKAGE", package.package_id, ":\n---------------------")
                print("ADDRESS:", package.address)
                print("DEADLINE:", package.deadline)
                print("CITY:", package.city)
                print("ZIP CODE:", package.zip_code)
                print("WEIGHT:", package.weight)
                print("DELIVERY STATUS:", package.status)
                print("DELIVERY TIME:", truck.delivery_times[i].strftime("%I:%M %p"), "\n")
                return
    print("Package #", package_id, " doesnt exist\n", sep="")


def hash_function(package_id):
    return int(package_id) % 10


def insert_package2(package, hash_table):
    hash_table2.insert(package)


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


class HashTable:
    def __init__(self):
        self.size = 10
        self.table = [None] * self.size

    def hash_function(self, key):
        return key % self.size

    def insert(self, package):
        index = self.hash_function(package.package_id)
        if self.table[index] is None:
            self.table[index] = package
        else:
            if not isinstance(self.table[index], list):
                self.table[index] = [self.table[index]]
            self.table[index].append(package)

    def search(self, package_id):
        index = self.hash_function(package_id)
        value = self.table[index]
        if isinstance(value, list):
            for item in value:
                if item.package_id == package_id:
                    return item
            return None
        elif value is not None:
            return value if value.package_id == package_id else None
        else:
            return None

    def remove(self, package_id):
        index = self.hash_function(package_id)
        value = self.table[index]
        if isinstance(value, list):
            for item in value:
                if item.package_id == package_id:
                    value.remove(item)
                    return
        elif value is not None:
            if value.package_id == package_id:
                self.table[index] = None


hash_table2 = HashTable()


class Truck:

    def __init__(self):
        self.packages = []
        self.delivery_times = []

    def add_package_by_id2(self, package_id, hash_table):
        packages = hash_table.search(package_id)
        if packages:
            if isinstance(packages, list):
                self.packages.extend(packages)
            else:
                self.packages.append(packages)
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

# 2
with open("packages.csv", 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        package_id, address, city, state, zip_code, deadline, weight, status = row
        package = Package(int(package_id), address, city, state, zip_code, deadline, weight, status)
        insert_package2(package, hash_table2)

"""
    CREATION OF TRUCK OBJECTS
"""

truck1 = Truck()
truck2 = Truck()
truck3 = Truck()
truck_list = [truck1, truck2, truck3]
"""
    TRUCK PACKAGE LOADING/SORTING
"""

truck1.add_package_by_id2(1, hash_table2)
truck1.add_package_by_id2(4, hash_table2)
truck1.add_package_by_id2(40, hash_table2)
truck1.add_package_by_id2(13, hash_table2)
truck1.add_package_by_id2(14, hash_table2)
truck1.add_package_by_id2(15, hash_table2)
truck1.add_package_by_id2(19, hash_table2)
truck1.add_package_by_id2(16, hash_table2)
truck1.add_package_by_id2(20, hash_table2)
truck1.add_package_by_id2(21, hash_table2)
truck1.add_package_by_id2(27, hash_table2)
truck1.add_package_by_id2(31, hash_table2)
truck1.add_package_by_id2(35, hash_table2)
truck1.add_package_by_id2(39, hash_table2)
truck1.add_package_by_id2(12, hash_table2)

truck2.add_package_by_id2(2, hash_table2)
truck2.add_package_by_id2(3, hash_table2)
truck2.add_package_by_id2(5, hash_table2)
truck2.add_package_by_id2(7, hash_table2)
truck2.add_package_by_id2(8, hash_table2)
truck2.add_package_by_id2(10, hash_table2)
truck2.add_package_by_id2(11, hash_table2)
truck2.add_package_by_id2(17, hash_table2)
truck2.add_package_by_id2(18, hash_table2)
truck2.add_package_by_id2(22, hash_table2)
truck2.add_package_by_id2(23, hash_table2)
truck2.add_package_by_id2(24, hash_table2)
truck2.add_package_by_id2(26, hash_table2)
truck2.add_package_by_id2(29, hash_table2)
truck2.add_package_by_id2(36, hash_table2)
truck2.add_package_by_id2(38, hash_table2)

truck3.add_package_by_id2(6, hash_table2)
truck3.add_package_by_id2(9, hash_table2)
truck3.add_package_by_id2(25, hash_table2)
truck3.add_package_by_id2(28, hash_table2)
truck3.add_package_by_id2(30, hash_table2)
truck3.add_package_by_id2(32, hash_table2)
truck3.add_package_by_id2(33, hash_table2)
truck3.add_package_by_id2(34, hash_table2)
truck3.add_package_by_id2(37, hash_table2)

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
    user_input1 = input(
        "What would you like to do? Lookup an individual package(1) OR Get status of all packages at a given time(2), or exit(3):")

    if user_input1 == "1":
        user_input2 = input("Please enter the package ID number:")
        result = lookup(int(user_input2))
    elif user_input1 == "2":
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

        print("--------------------- \n TOTAL MILES DRIVEN:\n---------------------")
        print(distance1 + distance2 + distance3)
    elif user_input1 == "3":
        print("Exiting the program.")
        break
    else:
        print("Please enter a valid option (1, 2, or 3)")
