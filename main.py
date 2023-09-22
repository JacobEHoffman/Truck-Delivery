# Author: Jacob Hoffman StudentID: 010840771
# C950 Data Structures & Algorithms PA

# Import of needed built-in python functions
import csv
import datetime
from builtins import ValueError


# Part A:
# HashTable class using chaining. Includes functions for initializing the hash table, inserting a new item, searching
# an item, and removing an item from the hash table. Used the function from the supplemental material Webinar 2
# Getting Greedy, who moved my data
# Space-Time Complexity of O(N)
class ChainingHashTable:
    # Creates an empty hash table with the size of initial_capacity
    def __init__(self, initial_capacity=39):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new item into the hash table.
    def insert(self, key, item):  # does both insert and update
        # uses the modulo operator to determine where the item will be inserted
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Part B:
    # Lookup and item in the hash table, allows the user to search using any variable in the package class
    def lookup(self, key):
        # uses the modulo operator to determine where the item will be found
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    # Removes an item from the hash table using a key as the constraint
    def remove(self, key):
        # uses the modulo operator to determine where the item to be removed will be found
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # If the key is found, removes the item correlated to the key
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])


# Class for package objects
# Space-Time Complexity of O(1)
class Package:
    def __init__(self, ID, Address, City, State, ZIP, Deadline, Weight, Notes, Status):
        self.ID = ID
        self.Address = Address
        self.City = City
        self.State = State
        self.ZIP = ZIP
        self.Deadline = Deadline
        self.Weight = Weight
        self.Notes = Notes
        self.Status = Status
        self.delivery_time = None
        self.departure_time = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.ID, self.Address, self.City, self.State,
                                                           self.ZIP, self.Deadline, self.Weight, self.Notes,
                                                           self.Status, self.delivery_time)

    def update_status(self, time):
        if time > self.delivery_time or time == self.delivery_time:
            self.Status = "Delivered"
        elif time > self.departure_time or time == self.departure_time:
            self.Status = "En route"
        else:
            self.Status = "At Hub"


# Loads package objects from the Packages.csv file and writes them into the hash table packageHash
# Space-Time Complexity of O(N)
def load_package_data(fileName):
    with open(fileName) as packages:
        packageData = csv.reader(packages, delimiter=',')
        for package in packageData:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZIP = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pNotes = package[7]
            pStatus = "ready to load"

            package = Package(pID, pAddress, pCity, pState, pZIP, pDeadline, pWeight, pNotes, pStatus)

            packageHash.insert(pID, package)


packageHash = ChainingHashTable()

load_package_data('Packages.csv')


# for i in range (len(packageHash.table)+1):
#    print("Key: {} and Package: {}".format(i+1, packageHash.search(i+1)))

# Class for truck objects
class Truck:
    def __init__(self, max_capacity, speed, distance_traveled, location, departure_time, packages):
        self.max_capacity = max_capacity
        self.speed = speed
        self.distance_traveled = distance_traveled
        self.location = location
        self.departure_time = departure_time
        self.packages = packages
        self.time = departure_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s" % (
            self.max_capacity, self.speed, self.distance_traveled, self.location, self.departure_time, self.packages)


# Reads the Distances.csv file
with open("Distances.csv") as distances:
    distanceData = csv.reader(distances, delimiter=',')
    distanceData = list(distanceData)


# Takes an address from either the package destination or truck location and returns the related row index from
# Distances.csv that is stored in the count variable
# Space-Time Complexity of O(N)
def get_address(address):
    count = 0
    for row in distanceData:
        if address in row[1]:
            return count
        else:
            count += 1


# Searches the Distances.csv file by row and column indexes that were found using the getAddress() function
# Space-Time Complexity of O(1)
def get_distance(row, col):
    if row is None:
        print("Nothing in row")
    if col is None:
        print("Nothing in col")
    distance = distanceData[row][col + 2]
    if distance == '':
        distance = distanceData[col][row + 2]

    return float(distance)


# Modified selection sort algorithm. Compares the distance between the truck location and the initial package
# address(i or index_smallest) with the distance between the truck location and the next package address(j).
# If the distance to j is less than the distance to i, then j becomes the new index_smallest and the process repeats,
# comparing the index_smallest[j] to the next item in line. Once the list is iterated through, the index_smallest item
# is swapped for the index i using a temp variable. This continues until the hash table is sorted, where the distance
# from the first package to the second package is the shortest distance between any of the other packages to each other,
# the distance of the second to third package is the second-shortest distance and so on. Thus, the distance between the
# last and second to last elements is the furthest distance between two items in the list
# Space-Time Complexity of O(N^2)
def selection_sorty(truck, packages):
    for i in range(len(packages) - 1):
        index_smallest = i
        for j in range(i + 1, len(packages)):
            if (get_distance(get_address(truck.location), get_address(packageHash.lookup(packages[j]).Address)) <
                    get_distance(get_address(truck.location),
                                 get_address(packageHash.lookup(packages[index_smallest]).Address))):
                index_smallest = j
        temp = packages[i]
        packages[i] = packages[index_smallest]
        packages[index_smallest] = temp


# Instantiation of truck objects for trucks 1, 2, and 3. I manually placed packages into the truck objects based
# on the given criteria. First looking at the delivery deadline, then what packages needed to be delivered together,
# then what packages were being delivered to the same address to minimize distance, then special notes were taken into
# account to ensure that packages were on truck 2 that had to be as well as packages only left the hub when they were
# at the depot.
truck1 = Truck(16, 18, 0, "HUB", datetime.timedelta(hours=8, minutes=0, seconds=0),
               [1, 4, 7, 8, 13, 14, 15, 16, 19, 20, 21, 29, 30, 34, 39, 40])

truck2 = Truck(16, 18, 0, "HUB", datetime.timedelta(hours=9, minutes=20, seconds=0),
               [2, 3, 5, 6, 9, 12, 18, 25, 26, 28, 31, 32, 33, 36, 37, 38])

truck3 = Truck(16, 18, 0, "HUB", datetime.timedelta(hours=10, minutes=30, seconds=0),
               [10, 11, 17, 22, 23, 24, 27, 35])


# Function to emulate the delivery of the packages. Takes a truck object as a parameter. First changes the address of
# package 9 to "410 S State St" because it will be delivered after 10:20 when the correct address is revealed.
# After using the selection sort to order packages according to the nearest neighbor algorithm, iterates through all
# packages that are loaded onto the truck object. Finds the distance between the location of the truck and the package
# delivery location. Records this distance, increments it to the truck's total distance traveled, and updates the
# truck's location to the newly delivered package's location. Updates the truck's time by dividing the distance
# traveled in miles by 18 miles per hour. Sets the package delivery time to the truck's current time and the package
# departure time to the truck's initial departure time. Once the for loop is finished executing, the total distance
# traveled is incremented one more time with the distance it takes to get from the truck's final delivery location
# back to the hub. Finally, changes the truck's location to "HUB" and updates its total distance traveled.
# Space-Time Complexity of O(N^2)
def package_delivery(truck):
    total_distance = 0
    selection_sorty(truck, truck.packages)

    for j in range(len(truck.packages)):
        distance_between_deliveries = get_distance(get_address(truck.location), get_address(packageHash.lookup(truck.packages[j]).Address))
        total_distance += distance_between_deliveries
        truck.distance_traveled = total_distance
        truck.location = packageHash.lookup(truck.packages[j]).Address
        truck.time += datetime.timedelta(hours=distance_between_deliveries / 18)
        if truck.time > datetime.timedelta(hours=10, minutes=20):
            if 9 in truck.packages:
                packageHash.lookup(9).Address = "410 S State St"
        packageHash.lookup(truck.packages[j]).delivery_time = truck.time
        packageHash.lookup(truck.packages[j]).departure_time = truck.departure_time
    total_distance += get_distance(get_address(truck.location), get_address("HUB"))
    truck.location = "HUB"
    truck.distance_traveled = total_distance


# The main class runs and offers the user an interface via the terminal to interact with the delivery data.
# First runs the package_delivery function for all three trucks, then greets the user and gives them the option to view
# package status or delivery truck distance traveled. If package status is selected, gives them the option to view
# a singular package or all at once at a given time. If delivery truck distance traveled is selected, gives the user
# the option to view the distance traveled of a singular truck or all trucks combined. Error handling is built-in to
# prevent the user from entering an invalid input.
class Main:
    package_delivery(truck1)
    package_delivery(truck2)
    package_delivery(truck3)
    menu_input = None
    while menu_input != "1" and menu_input != "2":
        print("Welcome to the WGUPS Main page, please enter the number for the option you would like:")
        print("1) Package Status")
        print("2) Delivery Truck Distance Traveled")
        menu_input = input("Please input an option number:")

        if menu_input == "1":
            package_input = None
            while package_input != "1" and package_input != "2":
                print("Would you like to view:")
                print("1) An individual package's status")
                print("2) All packages' statuses")
                package_input = input("Please input an option number:")
                if package_input == "1":
                    package_id_input = input("Please enter the package ID:")
                    time_to_display = input("Please enter the time that you would like to see the status(HH:MM:SS):")
                    (h, m, s) = time_to_display.split(":")
                    time_input = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    if package_id_input == "9":
                        if time_input < datetime.timedelta(hours=10, minutes=20):
                            packageHash.lookup(9).Address = "300 State St"
                    packageHash.lookup(int(package_id_input)).update_status(time_input)
                    if packageHash.lookup(int(package_id_input)).Status == "Delivered":
                        print(
                            str("PACKAGE ID: {:<2}, ADDRESS: {:<38}, CITY: {:<18}, STATE: {:<2}, ZIP: {:<5}, DEADLINE: {:<8}, WEIGHT: {:<2}, "
                                "STATUS: {:<9}, DELIVERY TIME: {}".format(packageHash.lookup(int(package_id_input)).ID,
                                                                          packageHash.lookup(int(package_id_input)).Address,
                                                                          packageHash.lookup(int(package_id_input)).City,
                                                                          packageHash.lookup(int(package_id_input)).State,
                                                                          packageHash.lookup(int(package_id_input)).ZIP,
                                                                          packageHash.lookup(int(package_id_input)).Deadline,
                                                                          packageHash.lookup(int(package_id_input)).Weight,
                                                                          packageHash.lookup(int(package_id_input)).Status,
                                                                          packageHash.lookup(int(package_id_input)).delivery_time
                                                                          )).replace(',', ' '))
                    else:
                        print(
                            str("PACKAGE ID: {:<2}, ADDRESS: {:<38}, CITY: {:<18}, STATE: {:<2}, ZIP: {:<5}, DEADLINE: {:<8}, WEIGHT: {:<2}, "
                                "STATUS: {:<9}, DELIVERY TIME: {}".format(packageHash.lookup(int(package_id_input)).ID,
                                                                          packageHash.lookup(int(package_id_input)).Address,
                                                                          packageHash.lookup(int(package_id_input)).City,
                                                                          packageHash.lookup(int(package_id_input)).State,
                                                                          packageHash.lookup(int(package_id_input)).ZIP,
                                                                          packageHash.lookup(int(package_id_input)).Deadline,
                                                                          packageHash.lookup(int(package_id_input)).Weight,
                                                                          packageHash.lookup(int(package_id_input)).Status,
                                                                          "Not Delivered")).replace(',', ' '))

                elif package_input == "2":
                    time_to_display = input("Please enter the time that you would like to see the statuses(HH:MM:SS):")
                    (h, m, s) = time_to_display.split(":")
                    time_input = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    if time_input < datetime.timedelta(hours=10, minutes=20):
                        packageHash.lookup(9).Address = "300 State St"
                    for packageID in range(len(packageHash.table) + 1):
                        packageHash.lookup(packageID+1).update_status(time_input)
                        if packageHash.lookup(packageID+1).Status == "Delivered":
                            print(
                                str("PACKAGE ID: {:<2}, ADDRESS: {:<38}, CITY: {:<18}, STATE: {:<2}, ZIP: {:<5}, DEADLINE: {:<8}, WEIGHT: {:<2}, "
                                    "STATUS: {:<9}, DELIVERY TIME: {}".format(packageHash.lookup(packageID + 1).ID,
                                                                              packageHash.lookup(packageID + 1).Address,
                                                                              packageHash.lookup(packageID + 1).City,
                                                                              packageHash.lookup(packageID + 1).State,
                                                                              packageHash.lookup(packageID + 1).ZIP,
                                                                              packageHash.lookup(packageID + 1).Deadline,
                                                                              packageHash.lookup(packageID + 1).Weight,
                                                                              packageHash.lookup(packageID + 1).Status,
                                                                              packageHash.lookup(packageID + 1).delivery_time
                                                                              )).replace(",", " "))
                        else:
                            print(
                                str("PACKAGE ID: {:<2}, ADDRESS: {:<38}, CITY: {:<18}, STATE: {:<2}, ZIP: {:<5}, DEADLINE: {:<8}, WEIGHT: {:<2}, "
                                    "STATUS: {:<9}, DELIVERY TIME: {}".format(packageHash.lookup(packageID + 1).ID,
                                                                              packageHash.lookup(packageID + 1).Address,
                                                                              packageHash.lookup(packageID + 1).City,
                                                                              packageHash.lookup(packageID + 1).State,
                                                                              packageHash.lookup(packageID + 1).ZIP,
                                                                              packageHash.lookup(
                                                                                  packageID + 1).Deadline,
                                                                              packageHash.lookup(packageID + 1).Weight,
                                                                              packageHash.lookup(packageID + 1).Status,
                                                                              "Not Delivered")).replace(",", " "))

        elif menu_input == "2":
            distance_input = None
            while distance_input != "1" and distance_input != "2" and distance_input != "3" and distance_input != "all":
                print("You can view the total distance traveled of each individual truck or all three combined")
                distance_input = input("To view an individual truck's distance, input its number, else type 'all'")
                if distance_input == "1":
                    print("Truck 1 total distance traveled: {}".format(truck1.distance_traveled))
                elif distance_input == "2":
                    print("Truck 2 total distance traveled: {}".format(truck2.distance_traveled))
                elif distance_input == "3":
                    print("Truck 3 total distance traveled: {}".format(truck3.distance_traveled))
                elif distance_input == "all":
                    print("Total Distance Traveled by all trucks: {}".format(truck1.distance_traveled +
                                                                             truck2.distance_traveled +
                                                                             truck3.distance_traveled))

# Truck 1 back in HUB at 10:22:00
# Truck 2 back in HUB at 11:53:00
# All Deliveries done at 12:40:20 and all trucks back at hub by 01:04:20
