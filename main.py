"""
    Sergio Pada
    Student ID: 001418359
"""
import csv

"""
    PROCESS/FLOW: Comments that use "#"
"""

from datetime import datetime, timedelta

"""
    INITIALIZATIONS
"""
wgu_address = "4001 S 700 E"
distances_table = []

"""
    FUNCTIONS
"""


# This lookup function looks up a package by its id and prints the package details. The function also takes in a time and based on that, prints a delivery status
def lookup(package_id, current_time):
    for truck in truck_list:
        if package_id in truck.package_ids:

            package = hash_table2.search(package_id)
            if package:
                print("--------------------- \n      Package", package.package_id, ":\n---------------------")
                print("Address:", package.address)
                print("Deadline:", package.deadline)
                print("City:", package.city)
                print("Zip Code:", package.zip_code)
                print("Weight:", package.weight)

                print("Delivery Status:", update_delivery_status(package_id, current_time))

                delivery_time = truck.delivery_times[truck.package_ids.index(package_id)]
                print("Delivery Time:", delivery_time.strftime("%I:%M %p"), "\n")
                return
    print("Package #", package_id, " doesn't exist\n", sep="")


# This function updates the status for a package given a time. This function used in the lookup function as well in order to display the delivery status
def update_delivery_status(package_id, current_time):
    truck = next((t for t in truck_list if package_id in t.package_ids), None)

    if truck is None:
        print("Package not found on any truck.")
        return

    index = truck.package_ids.index(package_id)
    delivery_time = truck.delivery_times[index]
    start_time = truck1.delivery_times[-1] if package_id in truck3.package_ids else datetime.strptime("08:00 AM",
                                                                                                      "%I:%M %p")
    if package_id in truck3.package_ids:
        start_time = truck1.delivery_times[-1]
    elif package_id in truck2.package_ids:
        datetime.strptime("09:10 AM", "%I:%M %p")
    else:
        datetime.strptime("08:00 AM", "%I:%M %p")
    package = hash_table2.search(package_id)

    if current_time < start_time:
        package.delivery_status = "At the Hub"
    elif current_time < delivery_time:
        package.delivery_status = "En Route"
    else:
        package.delivery_status = "Delivered"

    return package.delivery_status


# Simple hash function that returns an int 1-10
def hash_function(package_id):
    return int(package_id) % 10


# Finds row number that an address is located at within the addresses.csv file
def get_row_number(address):
    with open("addresses.csv", 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if row[0] == address:
                return i
    return None

# This uses distances_table to find the distance between 2 inputted addresses
def get_distance(address1, address2):
    row1 = get_row_number(address1)
    row2 = get_row_number(address2)
    return distances_table[row1][row2]


"""
    CLASSES
"""


# Class for package objects
class Package:
    # Constructor
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.status = status

# Class for hash table objects
class HashTable:
    # Constructor
    def __init__(self):
        self.size = 10
        self.table = [None] * self.size

    # This hashes a given value
    def hash_function(self, key):
        return key % self.size

    # This inserts a new package into the hash table
    def insert(self, package):
        index = self.hash_function(package.package_id)
        if self.table[index] is None:
            self.table[index] = package
        else:
            if not isinstance(self.table[index], list):
                self.table[index] = [self.table[index]]
            self.table[index].append(package)

    # This returns the package with an id that matches the input(if one exists)
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


# Instantiation of HashTable
hash_table2 = HashTable()

# Class for truck objects
class Truck:
    # Constructor
    def __init__(self):
        self.package_ids = []
        self.delivery_times = []

    # This adds a package id to the trucks package_ids list
    def add_package_id(self, package_id):
        self.package_ids.append(package_id)

    # This is the sorting method for the packages(nearest neighbor)
    def sort_packages_by_distance(self, wgu_address):
        sorted_package_ids = []
        unsorted_package_ids = self.package_ids.copy()

        current_address = wgu_address

        while unsorted_package_ids:
            def get_distance_from_current(package_id):
                package = hash_table2.search(package_id)
                return get_distance(current_address, package.address)

            nearest_package_id = min(unsorted_package_ids, key=get_distance_from_current)
            sorted_package_ids.append(nearest_package_id)
            unsorted_package_ids.remove(nearest_package_id)
            current_address = hash_table2.search(nearest_package_id).address

        self.package_ids = sorted_package_ids
    # This method creates a list of delivery times based on the sorted package ids associated address distances.
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

    # This method calculates the total distance travelled by a given truck
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
        elif self is truck1:
            base_time = datetime.strptime("08:00 AM", "%I:%M %p")
            if time < base_time:
                return 0
            elif time > self.delivery_times[-1]:
                elapsed_hours = (self.delivery_times[-1] - base_time).seconds / 3600
                return 18 * elapsed_hours
            else:
                elapsed_hours = (time - base_time).seconds / 3600
                return 18 * elapsed_hours
        else:
            base_time = datetime.strptime("09:10 AM", "%I:%M %p")
            if time < base_time:
                return 0
            elif time > self.delivery_times[-1]:
                elapsed_hours = (self.delivery_times[-1] - base_time).seconds / 3600
                return 18 * elapsed_hours
            else:
                elapsed_hours = (time - base_time).seconds / 3600
                return 18 * elapsed_hours


'''''
    POPULATION OF DISTANCE TABLE/CREATION OF PACKAGE OBJECTS
'''''
# This takes the data from distances.csv and inserts it into distance_table list
with open("distances.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        row_data = [float(value) for value in row]
        distances_table.append(row_data)

# This creates package objects with data taken from packages.csv
with open("packages.csv", 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        package_id, address, city, state, zip_code, deadline, weight, status = row
        package = Package(int(package_id), address, city, state, zip_code, deadline, weight, status)
        hash_table2.insert(package)

"""
    CREATION OF TRUCK OBJECTS
"""
# Truck instantiations
truck1 = Truck()
truck2 = Truck()
truck3 = Truck()
# Truck list used so that we can loop through all existing loaded packages.
truck_list = [truck1, truck2, truck3]
"""
    TRUCK PACKAGE LOADING/SORTING
"""
# Package objects are loaded onto the trucks


truck1.add_package_id(1)
truck1.add_package_id(13)
truck1.add_package_id(14)
truck1.add_package_id(15)
truck1.add_package_id(16)
truck1.add_package_id(19)
truck1.add_package_id(20)
truck1.add_package_id(29)
truck1.add_package_id(30)
truck1.add_package_id(31)
truck1.add_package_id(34)
truck1.add_package_id(37)
truck1.add_package_id(40)
truck2.add_package_id(38) #Needs to be on truck 2
truck1.add_package_id(39)
truck2.add_package_id(3)
truck3.add_package_id(25) #
truck2.add_package_id(6) #
truck2.add_package_id(18)
truck2.add_package_id(21)
truck2.add_package_id(28)#
truck2.add_package_id(36)
truck2.add_package_id(2)
truck2.add_package_id(4)
truck3.add_package_id(5)
truck3.add_package_id(7)
truck3.add_package_id(8)
truck3.add_package_id(9)
truck3.add_package_id(10)
truck3.add_package_id(11)
truck3.add_package_id(12)
truck3.add_package_id(17)
truck3.add_package_id(22)
truck3.add_package_id(23)
truck3.add_package_id(24)
truck3.add_package_id(26)
truck3.add_package_id(27)
truck3.add_package_id(32)
truck3.add_package_id(33)
truck3.add_package_id(35)

# Packages are sorted on the trucks
truck1.sort_packages_by_distance(wgu_address)
truck2.sort_packages_by_distance(wgu_address)
truck3.sort_packages_by_distance(wgu_address)

"""
    TRUCK DELIVERY TIME GENERATION
"""
# Delivery times for each package are generated
truck1.generate_delivery_times(datetime.strptime("8:00 AM", "%I:%M %p"), wgu_address)
truck2.generate_delivery_times(datetime.strptime("9:10 AM", "%I:%M %p"), wgu_address)
truck3.generate_delivery_times(truck1.delivery_times[-1], wgu_address)



"""
    UI
"""

print("*** ROUTING PROGRAM ***")
# The user picks an option
while True:
    user_input1 = input(
        "What would you like to do?\n   (1)Lookup the status of an individual package\n   (2)Get status of all packages at a given time\n   (3)Exit\nEnter a number:")

    if user_input1 == "1":
        # If the user wants to view the status of an individual package, then they're prompted to enter a package id and time the package's status is updated and printed to screen.
        user_input2 = input("Please enter the package ID number: ")

        user_input_time = input("Please enter a time: ")
        time_format = "%I:%M %p"

        try:
            input_datetime = datetime.strptime(user_input_time, time_format)
        except ValueError:
            print("Invalid time format. Please enter the time in the format HH:MM AM/PM")

        update_delivery_status(int(user_input2), input_datetime)
        print(hash_table2.search(int(user_input2)).delivery_status)
    elif user_input1 == "2":
        # If the user wants to view the information on each package, then they are prompted to enter a time. For each package inside each truck, the package's id and the user inputted time are passed into the lookup function which displays each packages info.
        while True:
            user_input_time = input("Enter a time (Including AM or PM): ")

            try:
                user_input_time = datetime.strptime(user_input_time, "%I:%M %p")
                break
            except ValueError:
                print("Invalid format. Please enter the time in the format Hour:Minute AM/PM")

        print("--------------------- \n      TRUCK 1:\n---------------------")

        for package_id in truck1.package_ids:
            lookup(package_id, user_input_time)

        distance1 = truck1.calculate_distance(user_input_time)
        print("\nDistance traveled:", distance1, "miles\n")
        print("--------------------- \n      TRUCK 2:\n---------------------")

        for package_id in truck2.package_ids:
            lookup(package_id, user_input_time)
        distance2 = truck2.calculate_distance(user_input_time)
        print("\nDistance traveled:", distance2, "miles\n")

        print("--------------------- \n      TRUCK 3:\n---------------------")

        for package_id in truck3.package_ids:
            lookup(package_id, user_input_time)

        distance3 = truck3.calculate_distance(user_input_time)
        print("\nDistance traveled:", distance3, "miles\n")

        print("--------------------- \n TOTAL MILES DRIVEN:\n---------------------")
        print(distance1 + distance2 + distance3)
    elif user_input1 == "3":
        # If the user picks "Exit", then the program is terminated
        print("Exiting the program.")
        break
    else:
        print("Please enter a valid option (1, 2, or 3)")

