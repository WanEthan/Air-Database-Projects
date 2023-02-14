""" This program asks for the user to type his/her name to get a polite
reply and then ask them for picking up an option from the main menu by
entering its number only.

"""

from enum import Enum
import csv

filename = './purple_air.csv'  # Create a global string object for the file


class EmptyDatasetError(Exception):
    """ Raises this custom exception while asking a method without data
    on the dataset

    """
    pass


class NoMatchingItems(Exception):
    """ Raises this custom exception while the _cross_table_statistics
    function fails to find any data that matches the two parameters

    """
    pass


class Stats(Enum):
    """ Create MIN, AVG, and MAX entries and assign values to each
    entry that meet the correct position in the return tuple value of
    _cross_table_statistics()

    """
    MIN = 0
    AVG = 1
    MAX = 2


class DataSet:
    """ Add a DataSet class

    Attributes:
    header (str), data (none), zip_codes (list), time (list)

    """

    def __init__(self, header=""):
        """ Initializes a dataset object """
        self._data = None
        self.header = header
        self._zips = {}
        self._times = []

    @property
    def header(self):
        """ Make the header without directly using the _header
        attribute

        """
        return self._header

    @header.setter
    def header(self, header=""):
        """ Check the length of the header is less than or equal to 30

        """
        if len(header) <= 30:
            self._header = header
        else:
            raise ValueError

    def get_zips(self):
        """ Make zip codes without directly using the _zips
        attribute

        """
        copy_zip_codes = self._zips.copy()
        return copy_zip_codes

    def toggle_zip(self, target_zip: str):
        """ Check zip codes in dictionary and flip its boolean value;
        if not, raising a LookupError

        """
        if target_zip in self._zips:
            self._zips[target_zip] = not self._zips[target_zip]
        else:
            raise LookupError

    def _initialize_labels(self):
        """ Create two sets to hold zip codes and times of day;
        Using a for loop to go through every item in self._data and add
        each item of zip code and the time to zip code set and the time
        of day set;
        Assign the both sets to self._zips and self._times

        """
        zip_codes = {}  # initialize self._zips to an empty dictionary
        the_time_of_day = set()
        for item in self._data:
            zip_codes[item[0]] = True
            the_time_of_day.add(item[1])
        self._zips = zip_codes
        self._times = list(the_time_of_day)

    def _cross_table_statistics(self, descriptor_one: str,
                                descriptor_two: str):
        """ Apply a list comprehension to make a lost of concentration
        for the data that match the two parameters;
        Raise EmptyDatasetError if no self._data;
        Raise NoMatchingItems if no matching both descriptors;
        assign the list of concentration in the order of the min, ave,
        and max concentration as a tuple of floats;
        return the assignment

        """
        if not self._data:
            raise EmptyDatasetError
        my_list = [row[2] for row in self._data if row[0] == descriptor_one
                   and row[1] == descriptor_two]
        if not my_list:
            raise NoMatchingItems
        a_tuple_of_float = (min(my_list), sum(my_list) / len(my_list),
                            max(my_list))
        return a_tuple_of_float

    def load_file(self):
        """ load data from purple_air.csv by using the global object to
        specify the file to open

        """
        with open(filename, newline='') as f:
            the_file_data = csv.reader(f)
            next(the_file_data)  # Remove the header row
            self._data = []
            for line in the_file_data:
                my_selected_data = (line[1], line[4], float(line[5]))
                # Create a tuple that only contain zip code, time of day and
                # concentration for each line
                self._data.append(my_selected_data)
            the_total_lines = len(self._data)  # Find many lines are loaded
            print(f"There are {the_total_lines} lines loaded")
            self._initialize_labels()

    def manage_filters(self, my_dataset):
        """ If no dataset, print a message and return to the main menu;
        if dataset exits, Using the loop to print a menu and ask users
        to toggle one of the items by entering its associated number;
        Also, check for bad user inputs

        """
        if not self._data:
            print("Please enter the load Data option first!")
            return
        while True:
            print("The following labels are in the dataset: ")
            for menu_number, item in enumerate(self.get_zips(), 1):
                zipcode_state = "ACTIVE" if self.get_zips()[item] is True \
                    else "INACTIVE"
                print(f"{menu_number}: {item:10}{zipcode_state}")
            a_toggle_number = input("Please choose an item to toggle or "
                                    "press enter/return if you are "
                                    "finished.")
            try:
                if not a_toggle_number:
                    break  # exit the loop
                else:
                    a_toggle_number = int(a_toggle_number)
                    # convert str to int
            except ValueError:
                print("Please only enter a number, thank you!")
                continue  # ask the user to select a number again
            a_list_zipcode = list(self.get_zips())
            if 1 <= a_toggle_number <= 8:
                a_toggle_number -= 1
                # convert inputs to computer-readable form
                zipcode = a_list_zipcode[a_toggle_number]
                my_dataset.toggle_zip(zipcode)
            else:
                print("This number is not on the menu.")

    def display_cross_table(self, stat: Stats):
        """ When data is loaded, print a table to show min, avg, or max
        values of each pair of zip code and time of day;
        Output values are determined by a user's selection

        """
        if not self._data:
            print("Please enter the load Data option first!")
            return
        if True:
            filtered_zips = [a_key for a_key in self._zips if
                             self._zips[a_key] is True]
            print()
            print(end="        ")
            for times in self._times:  # print times horizontally
                print(f"{times:>9}", end="")
            print()
            for zip_code in filtered_zips:
                print(f"{zip_code:<8}", end="")  # print zip codes vertically
                for times in self._times:  # print min, avg or max values
                    # based on using the Enum value as an argument
                    try:
                        data_tuple = self._cross_table_statistics(
                            zip_code, times)
                        print(f"{data_tuple[stat.value]:>9.2f}", end="")
                    except NoMatchingItems:
                        no_number = "N/A"
                        print(f"{no_number:>9}", end="")
                print()


def print_menu():
    """ Print the all lists of the menu """
    print("Main Menu")
    print("1 - Print Average Particulate Concentration by Zip Code and time")
    print("2 - Print Minimum Particulate Concentration by Zip Code and time")
    print("3 - Print Maximum Particulate Concentration by Zip Code and time")
    print("4 - Adjust Zip Code Filters")
    print("5 - Load Data")
    print("9 - Quit")


def menu(my_dataset):
    """ Use the while function to print the menu and my dataset header
    and check the user's input is valid, invalid or something else.

    """
    while True:
        print()
        print(my_dataset.header)
        print_menu()
        selected_number = input("Which option would you like to pick up? ")
        try:
            the_selection = int(selected_number)  # convert str to int
        except ValueError:
            print("Please only enter a number, thank you!")
            continue  # ask the user to select a number again
        if the_selection == 9:
            print("Goodbye! Thank you for using the data system.")
            break  # exit the loop
        elif the_selection == 1:
            my_dataset.display_cross_table(Stats.AVG)
        elif the_selection == 2:
            my_dataset.display_cross_table(Stats.MIN)
        elif the_selection == 3:
            my_dataset.display_cross_table(Stats.MAX)
        elif the_selection == 4:
            my_dataset.manage_filters(my_dataset)
        elif the_selection == 5:
            my_dataset.load_file()
        else:
            print("This number is not on the menu.")


def main():
    """ run the unit test function;
    Get the user's name and print a greeting reply;
    create an DataSet object called purple_air;
    Keep asking the user for a header until a valid input is entered;
    Print menu with a valid header

    """
    your_first_name = input("Please provide me your first name: ")
    print("Hello ", your_first_name, ",",
          " I hope you're having a good day. Here is the Air Quality "
          "Database.", sep="")
    purple_air = DataSet()
    while True:
        message = input("Enter a header for the menu:\n")
        try:
            purple_air.header = message
        except ValueError:
            print("Please only enter a string less or equal to than 30"
                  "characters long")
            continue  # ask the user to type a header again
        menu(purple_air)
        break


if __name__ == "__main__":
    main()

"""

-----sample run-----

Please provide me your first name: Ethan
Hello Ethan, I hope you're having a good day. Here is the Air Quality Database.
Enter a header for the menu:
Data for a cleaner world

Data for a cleaner world
Main Menu
1 - Print Average Particulate Concentration by Zip Code and time
2 - Print Minimum Particulate Concentration by Zip Code and time
3 - Print Maximum Particulate Concentration by Zip Code and time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
Which option would you like to pick up? 1
Please enter the load Data option first!

Data for a cleaner world
Main Menu
1 - Print Average Particulate Concentration by Zip Code and time
2 - Print Minimum Particulate Concentration by Zip Code and time
3 - Print Maximum Particulate Concentration by Zip Code and time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
Which option would you like to pick up? 5
There are 6147 lines loaded

Data for a cleaner world
Main Menu
1 - Print Average Particulate Concentration by Zip Code and time
2 - Print Minimum Particulate Concentration by Zip Code and time
3 - Print Maximum Particulate Concentration by Zip Code and time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
Which option would you like to pick up? 1

            Night   Midday  Morning  Evening
94028        1.58     2.92     1.54     2.26
94304        1.23     2.89     1.36     1.17
94022        1.32     2.92     1.50     1.22
94024        1.69     3.27     1.71     3.42
94040        2.47     3.28     1.86     4.57
94087        2.31     3.92     2.24     4.77
94041        3.43     3.52     2.41     4.53
95014        2.19     3.29     1.06     2.38

Data for a cleaner world
Main Menu
1 - Print Average Particulate Concentration by Zip Code and time
2 - Print Minimum Particulate Concentration by Zip Code and time
3 - Print Maximum Particulate Concentration by Zip Code and time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
Which option would you like to pick up? 2

            Night   Midday  Morning  Evening
94028        0.00     0.00     0.00     0.00
94304        0.00     0.00     0.00     0.00
94022        0.00     0.00     0.00     0.00
94024        0.00     0.00     0.00     0.00
94040        0.00     0.00     0.00     0.00
94087        0.00     0.00     0.00     0.00
94041        0.00     0.00     0.00     0.00
95014        0.00     0.00     0.00     0.00

Data for a cleaner world
Main Menu
1 - Print Average Particulate Concentration by Zip Code and time
2 - Print Minimum Particulate Concentration by Zip Code and time
3 - Print Maximum Particulate Concentration by Zip Code and time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
Which option would you like to pick up? 3

            Night   Midday  Morning  Evening
94028       25.00    24.21    25.72    79.88
94304        9.92    20.93     9.66     9.73
94022       14.38    26.59    12.90    11.53
94024        9.67    29.17    15.12    37.57
94040       20.34    25.95    10.49    44.05
94087       13.14    26.48     9.39    38.11
94041       19.67    25.89     8.02    31.82
95014       37.82    25.00     9.95    69.05

Data for a cleaner world
Main Menu
1 - Print Average Particulate Concentration by Zip Code and time
2 - Print Minimum Particulate Concentration by Zip Code and time
3 - Print Maximum Particulate Concentration by Zip Code and time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
Which option would you like to pick up? 4
The following labels are in the dataset: 
1: 94028     ACTIVE
2: 94304     ACTIVE
3: 94022     ACTIVE
4: 94024     ACTIVE
5: 94040     ACTIVE
6: 94087     ACTIVE
7: 94041     ACTIVE
8: 95014     ACTIVE
Please choose an item to toggle or press enter/return if you are finished.8
The following labels are in the dataset: 
1: 94028     ACTIVE
2: 94304     ACTIVE
3: 94022     ACTIVE
4: 94024     ACTIVE
5: 94040     ACTIVE
6: 94087     ACTIVE
7: 94041     ACTIVE
8: 95014     INACTIVE
Please choose an item to toggle or press enter/return if you are finished.

Data for a cleaner world
Main Menu
1 - Print Average Particulate Concentration by Zip Code and time
2 - Print Minimum Particulate Concentration by Zip Code and time
3 - Print Maximum Particulate Concentration by Zip Code and time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
Which option would you like to pick up? 3

            Night   Midday  Morning  Evening
94028       25.00    24.21    25.72    79.88
94304        9.92    20.93     9.66     9.73
94022       14.38    26.59    12.90    11.53
94024        9.67    29.17    15.12    37.57
94040       20.34    25.95    10.49    44.05
94087       13.14    26.48     9.39    38.11
94041       19.67    25.89     8.02    31.82

Data for a cleaner world
Main Menu
1 - Print Average Particulate Concentration by Zip Code and time
2 - Print Minimum Particulate Concentration by Zip Code and time
3 - Print Maximum Particulate Concentration by Zip Code and time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
Which option would you like to pick up? 9
Goodbye! Thank you for using the data system.

Process finished with exit code 0

"""