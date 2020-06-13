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
first_names_present = []
last_names_present = []
first_names_hours = []
last_names_hours = []

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

pickle_in = open('Updating Hours Files/updating_hours_firstname.pickle', 'rb')
first_names_hours = pickle.load(pickle_in)

pickle_in = open('Updating Hours Files/updating_hours_lastname.pickle', 'rb')
last_names_hours = pickle.load(pickle_in)

hours_list = []


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
                current_hours_list = get_hours(first_names_hours, last_names_hours)
                hours_gained = input(f'Input the number of new hours for {name}: ')
                total_hours = float(current_hours_list[index]) + float(hours_gained)
                print('New Total:', total_hours)
                sheet.update_cell(cell.row, 32, total_hours)


def get_hours(first_names, last_names):
    for index, name in enumerate(first_names):
        for list in list_of_lists:
            if name == list[1] and last_names[index] == list[0]:
                if list[31] == ' ':
                    hours_list.append(list[31])
                else:
                    hours_list.append(0)
    return hours_list


# print(get_hours(first_names_hours, last_names_hours))
# set_hours(first_names_hours, last_names_hours)


# def get_least_active
''' Have to check number of hours, 0 1 or 2 events, 
'''

# def meeting_requirement



