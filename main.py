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
        if package_id in truck.package_ids:
            package = hash_table2.search(package_id)
            if package:
                print("--------------------- \n      PACKAGE", package.package_id, ":\n---------------------")
                print("ADDRESS:", package.address)
                print("DEADLINE:", package.deadline)
                print("CITY:", package.city)
                print("ZIP CODE:", package.zip_code)
                print("WEIGHT:", package.weight)
                print("DELIVERY STATUS:", package.status)
                truck_index = truck_list.index(truck)
                delivery_time = truck.delivery_times[truck.package_ids.index(package_id)]
                print("DELIVERY TIME:", delivery_time.strftime("%I:%M %p"), "\n")
                return
    print("Package #", package_id, " doesn't exist\n", sep="")



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
        self.package_ids = []  # Store package IDs instead of packages
        self.delivery_times = []

    def add_package_id(self, package_id):
        self.package_ids.append(package_id)
    # def add_package_by_id2(self, package_id, hash_table):
    #     packages = hash_table.search(package_id)
    #     if packages:
    #         if isinstance(packages, list):
    #             self.packages.extend(packages)
    #         else:
    #             self.packages.append(packages)
    #         return True
    #     return False

    def sort_packages_by_distance(self, wgu_address):
        sorted_package_ids = []  # New list to store sorted package IDs
        unsorted_package_ids = self.package_ids.copy()

        def get_distance_from_wgu(package_id):
            package = hash_table2.search(package_id)
            return get_distance(wgu_address, package.address)

        furthest_package_id = max(unsorted_package_ids, key=get_distance_from_wgu)

        sorted_package_ids.append(furthest_package_id)
        unsorted_package_ids.remove(furthest_package_id)

        current_address = hash_table2.search(furthest_package_id).address

        while unsorted_package_ids:
            def get_distance_from_current(package_id):
                package = hash_table2.search(package_id)
                return get_distance(current_address, package.address)

            nearest_package_id = min(unsorted_package_ids, key=get_distance_from_current)
            sorted_package_ids.append(nearest_package_id)
            unsorted_package_ids.remove(nearest_package_id)
            current_address = hash_table2.search(nearest_package_id).address

        self.package_ids = sorted_package_ids

    def generate_delivery_times(self, start_time, wgu_address):
        delivery_times = []
        current_time = start_time
        last_address = wgu_address

        for package_id in self.package_ids:
            package = hash_table2.search(package_id)
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

        for package_id, delivery_time in zip(self.package_ids, self.delivery_times):
            package = hash_table2.search(package_id)
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

truck1.add_package_id(1)
truck1.add_package_id(4)
truck1.add_package_id(40)
truck1.add_package_id(13)
truck1.add_package_id(14)
truck1.add_package_id(15)
truck1.add_package_id(19)
truck1.add_package_id(16)
truck1.add_package_id(20)
truck1.add_package_id(21)
truck1.add_package_id(27)
truck1.add_package_id(31)
truck1.add_package_id(35)
truck1.add_package_id(39)
truck1.add_package_id(12)

truck2.add_package_id(2)
truck2.add_package_id(3)
truck2.add_package_id(5)
truck2.add_package_id(7)
truck2.add_package_id(8)
truck2.add_package_id(10)
truck2.add_package_id(11)
truck2.add_package_id(17)
truck2.add_package_id(18)
truck2.add_package_id(22)
truck2.add_package_id(23)
truck2.add_package_id(24)
truck2.add_package_id(26)
truck2.add_package_id(29)
truck2.add_package_id(36)
truck2.add_package_id(38)

truck3.add_package_id(6)
truck3.add_package_id(9)
truck3.add_package_id(25)
truck3.add_package_id(28)
truck3.add_package_id(30)
truck3.add_package_id(32)
truck3.add_package_id(33)
truck3.add_package_id(34)
truck3.add_package_id(37)

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

        for package_id in truck1.package_ids:
            package = hash_table2.search(package_id)
            print("Package ", package_id, ": ", package.delivery_status, sep="")

        distance1 = truck1.calculate_distance(user_input_time)
        print("\nDistance traveled:", distance1, "miles\n")
        print("--------------------- \n      TRUCK 2:\n---------------------")
        truck2.update_delivery_status(user_input_time)

        for package_id in truck2.package_ids:
            package = hash_table2.search(package_id)
            print("Package ", package_id, ": ", package.delivery_status, sep="")
        distance2 = truck2.calculate_distance(user_input_time)
        print("\nDistance traveled:", distance2, "miles\n")

        print("--------------------- \n      TRUCK 3:\n---------------------")
        truck3.update_delivery_status(user_input_time)

        for package_id in truck3.package_ids:
            package = hash_table2.search(package_id)
            print("Package ", package_id, ": ", package.delivery_status, sep="")

        distance3 = truck3.calculate_distance(user_input_time)
        print("\nDistance traveled:", distance3, "miles\n")

        print("--------------------- \n TOTAL MILES DRIVEN:\n---------------------")
        print(distance1 + distance2 + distance3)
    elif user_input1 == "3":
        print("Exiting the program.")
        break
    else:
        print("Please enter a valid option (1, 2, or 3)")
