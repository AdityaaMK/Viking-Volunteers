import gspread
import csv
import time
from oauth2client.service_account import ServiceAccountCredentials
import pickle
from pprint import pprint


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)

# Open the spreadsheet
sheet = client.open('test').sheet1

# Get a list of all records
data = sheet.get_all_records()

# Get 2D list of all records
list_of_lists = sheet.get_all_values()

id_numbers = []
hours_list = []
first_names_present = []
last_names_present = []
first_names_hours = []
last_names_hours = []
first_names_events = []
last_names_events = []

# For Attendance

# with open('Attendance Files/attendance_id_numbers.csv') as file:
#     reader = csv.reader(file)
#
#     for index, row in enumerate(reader):
#         if index != 0:
#             id_numbers.append(row[0])
#
#     pickle_out = open('Attendance Files/id.pickle', 'wb')
#     pickle.dump(id_numbers, pickle_out)
#     pickle_out.close()

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


def update_attendance(id_nums):
    for index, tag in enumerate(id_nums):
        for row in list_of_lists:
            if tag == row[2]:
                cell = sheet.find(tag)
                sheet.update_cell(cell.row, 12, "Y")  # Modify 12 to other column numbers as necessary for attendance
                time.sleep(10)


# def update_attendance2(first_names, last_names):
#     for index, name in enumerate(first_names):
#         for list in list_of_lists:
#             if name == list[1] and last_names[index] == list[0]:
#                 cell = sheet.find(name)
#                 sheet.update_cell(cell.row, 13, "Y")


# update_attendance(id_numbers)


def qsort(inlist):
    if not inlist:
        return []
    else:
        pivot = inlist[0]
        print(pivot)
        lesser = qsort([x for x in inlist[1:] if x < pivot])
        print(lesser)
        greater = qsort([x for x in inlist[1:] if x >= pivot])
        print(greater)
        return lesser + [pivot] + greater


def set_hours(first_names, last_names):
    for index, name in enumerate(first_names):
        for list in list_of_lists:
            if name == list[1] and last_names[index] == list[0]:
                cell = sheet.find(name)
                current_hours_list = []
                current_hours_list = get_hours(first_names, last_names, current_hours_list)
                hours_gained = input(f'Input the number of new hours for {name}: ')
                total_hours = float(current_hours_list[index]) + float(hours_gained)
                print('New Total:', total_hours)
                sheet.update_cell(cell.row, 30, total_hours)


def get_hours(first_names, last_names, hours_data):
    for index, name in enumerate(first_names):
        for list in list_of_lists:
            if name == list[1] and last_names[index] == list[0]:
                if list[29] == ' ':
                    hours_data.append(0)
                else:
                    hours_data.append(list[29])
    return hours_data


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


def get_least_active():
    # TODO Have to check number of hours, 0 1 or 2 events,
    insertion_sort(hours_list, first_names_events, last_names_events)

    qualified = []
    num_events = []

    for index, name in enumerate(first_names_events):
        for list in list_of_lists:
            if name == list[1] and last_names_events[index] == list[0]:
                cell = sheet.find(name)
                if sheet.cell(cell.row, 9).value == 'Y' and sheet.cell(cell.row, 10).value == 'Y' and sheet.cell(cell.row, 9).value == 'Y':
                    qualified.append("Qualified")
                else:
                    qualified.append("Not Qualified")
                if sheet.cell(cell.row, 28).value == 'Y' and sheet.cell(cell.row, 29).value == 'Y':
                    num_events.append(2)
                elif sheet.cell(cell.row, 28).value == 'Y' or sheet.cell(cell.row, 29).value == 'Y':
                    num_events.append(1)
                else:
                    num_events.append(0)

    for index, hour in enumerate(hours_list):
        if qualified[index] == "Qualified":
            print(f"Forms: Yes\tEvents: {num_events[index]}\tHours: {hour}\tName: {first_names_events[index]} {last_names_events[index]}")
        else:
            print(f"Forms: No\tEvents: {num_events[index]}\tHours: {hour}\tName: {first_names_events[index]} {last_names_events[index]}")


# hours_list = get_hours(first_names_events, last_names_events, hours_list)
# pickle_out = open('Event Selection Files/selecting_events_hours_list.pickle', 'wb')
# pickle.dump(hours_list, pickle_out)
# pickle_out.close()

# Make sure pickled data is up to date
pickle_in = open('Event Selection Files/selecting_events_hours_list.pickle', 'rb')
hours_list = pickle.load(pickle_in)

# Converting strings in list to floats
hours_list = list(map(float, hours_list))

get_least_active()
# set_hours(first_names_events, last_names_events)

# def meeting_requirement



