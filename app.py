"""
    File name: app.py
    Author: Adityaa Magesh Kumar
    Date created: 6/12/2020
    Date last modified: 6/16/2020
    Python Version: 3.8
"""

import gspread
import csv
import time
from oauth2client.service_account import ServiceAccountCredentials
import pickle
from pprint import pprint


# List Objects
id_numbers = []
hours_list = []
first_names_present = []
last_names_present = []
first_names_hours = []
last_names_hours = []
first_names_events = []
last_names_events = []


# Setup and linking to spreadsheet
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open('test').sheet1  # Open the spreadsheet
list_of_lists = sheet.get_all_values()  # Get 2D list of all records


# For Attendance
with open('Attendance Files/attendance_id_numbers.csv') as file:
    reader = csv.reader(file)

    for index, row in enumerate(reader):
        if index != 0:
            id_numbers.append(row[0])

    pickle_out = open('Attendance Files/id.pickle', 'wb')
    pickle.dump(id_numbers, pickle_out)
    pickle_out.close()
pickle_in = open('Attendance Files/id.pickle', 'rb')
id_numbers = pickle.load(pickle_in)


# For Updating Hours
# with open('Updating Hours Files/updating_hours_first_and_last_names.csv') as file:
#     reader = csv.reader(file)
#
#     for index, row in enumerate(reader):
#         first_names_hours.append(row[1])
#         last_names_hours.append(row[0])
#
#     pickle_out = open('Updating Hours Files/updating_hours_firstname.pickle', 'wb')
#     pickle.dump(first_names_hours, pickle_out)
#     pickle_out.close()
#
#     pickle_out = open('Updating Hours Files/updating_hours_lastname.pickle', 'wb')
#     pickle.dump(last_names_hours, pickle_out)
#     pickle_out.close()
#
# pickle_in = open('Updating Hours Files/updating_hours_firstname.pickle', 'rb')
# first_names_hours = pickle.load(pickle_in)
#
# pickle_in = open('Updating Hours Files/updating_hours_lastname.pickle', 'rb')
# last_names_hours = pickle.load(pickle_in)


# For Event Selection
# with open('Event Selection Files/selecting_events_fullnames.csv') as file:
#     reader = csv.reader(file)
#
#     for index, row in enumerate(reader):
#         first_names_events.append(row[1])
#         last_names_events.append(row[0])
#
#     pickle_out = open('Event Selection Files/selecting_events_fullnames.pickle', 'wb')
#     pickle.dump((first_names_events, last_names_events), pickle_out)
#     pickle_out.close()
with open('Event Selection Files/selecting_events_fullnames.pickle', 'rb') as file:
    all_names = pickle.load(file)
    first_names_events = all_names[0]
    last_names_events = all_names[1]
# for index, i in enumerate(last_names_events):
#     print(f"{i}, {first_names_events[index]}")


# All Functions below
def update_attendance(id_nums):
    for index, tag in enumerate(id_nums):
        for index2, row in enumerate(list_of_lists):
            if tag == row[2]:
                sheet.update_cell(index2+1, 12, "Y")  # Modify 12 to other column numbers as necessary for attendance
                time.sleep(5)

# Second way to update attendance if necessary
# def update_attendance2(first_names, last_names):
#     for index, name in enumerate(first_names):
#         for list in list_of_lists:
#             if name == list[1] and last_names[index] == list[0]:
#                 cell = sheet.find(name)
#                 sheet.update_cell(cell.row, 13, "Y")


def set_hours(first_names, last_names):
    for index, name in enumerate(first_names):
        for index2, list in enumerate(list_of_lists):
            if name == list[1] and last_names[index] == list[0]:
                current_hours_list = []
                current_hours_list = get_hours(first_names, last_names, current_hours_list)
                hours_gained = input(f'Input the number of new hours for {name}: ')
                if hours_gained.lower() == 'stop':
                    return
                total_hours = float(current_hours_list[index]) + float(hours_gained)
                print('New Total:', total_hours)
                sheet.update_cell(index2+1, 30, total_hours)


# Returns hours for set_hours function and hours_list
def get_hours(first_names, last_names, hours_data):
    for index, name in enumerate(first_names):
        for list in list_of_lists:
            if name == list[1] and last_names[index] == list[0]:
                if list[29] == ' ':
                    hours_data.append(0)
                else:
                    hours_data.append(list[29])
    return hours_data


# Returns sorted list for least active function
def insertion_sort(arr, firstnames, lastnames):
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):

        key = arr[i]
        key2 = firstnames[i]
        key3 = lastnames[i]

        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            firstnames[j + 1] = firstnames[j]
            lastnames[j + 1] = lastnames[j]
            j -= 1
        arr[j + 1] = key
        firstnames[j + 1] = key2
        lastnames[j + 1] = key3


# Returns least active members to use for event selection
def get_least_active():
    # MAKE SURE HOURS_LIST PICKLED DATA IS UP TO DATE!!!
    insertion_sort(hours_list, first_names_events, last_names_events)

    qualified = []
    num_events = []

    for index, name in enumerate(first_names_events):
        for list in list_of_lists:
            if name == list[1] and last_names_events[index] == list[0]:
                # cell = sheet.find(name)
                event_one = list[27]
                event_two = list[28]
                if list[8] == 'Y' and list[9] == 'Y' and list[10] == 'Y':
                    qualified.append("Qualified")
                else:
                    qualified.append("Not Qualified")
                if event_one == 'Y' and event_two == 'Y':
                    num_events.append(2)
                elif event_one == 'Y' or event_two == 'Y':
                    num_events.append(1)
                else:
                    num_events.append(0)

    for index, hour in enumerate(hours_list):
        if qualified[index] == "Qualified":
            print(f"Forms: Yes\tEvents: {num_events[index]}\tHours: {hour}\tName: {first_names_events[index]} {last_names_events[index]}")
        else:
            print(f"Forms: No\tEvents: {num_events[index]}\tHours: {hour}\tName: {first_names_events[index]} {last_names_events[index]}")


# Checks if user completed meeting requirement, and will add other spreadsheet functions later
# def meeting_requirement


# MAKE SURE HOURS_LIST PICKLED DATA IS UP TO DATE!!!
hours_list = get_hours(first_names_events, last_names_events, hours_list)
pickle_out = open('Event Selection Files/selecting_events_hours_list.pickle', 'wb')
pickle.dump(hours_list, pickle_out)
pickle_out.close()

pickle_in = open('Event Selection Files/selecting_events_hours_list.pickle', 'rb')
hours_list = pickle.load(pickle_in)

# Converting strings in list to floats
hours_list = list(map(float, hours_list))


# Function calls at end of program
update_attendance(id_numbers)

# get_least_active()

# set_hours(first_names_events, last_names_events)


