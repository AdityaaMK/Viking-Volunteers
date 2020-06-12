import gspread
from oauth2client.service_account import ServiceAccountCredentials
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

# TODO USE ID NUMBERS INSTEAD
first_names_present = ['Aditya', 'Aditya', 'Jai']
last_names_present = ['Adhikari', 'Agrawal', 'Agrawal']

first_names_hours = ['Aditya', 'Aditya', 'Jai']
last_names_hours = ['Adhikari', 'Agrawal', 'Agrawal']

hours_list = []


def update_attendance(first_names, last_names):
    for index, name in enumerate(first_names):
        for list in list_of_lists:
            if name == list[1] and last_names[index] == list[0]:
                cell = sheet.find(name)
                sheet.update_cell(cell.row, 13, "Y")


update_attendance(first_names_present, last_names_present)


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


print(get_hours(first_names_hours, last_names_hours))
set_hours(first_names_hours, last_names_hours)


# def get_least_active
''' Have to check number of hours, 0 1 or 2 events, 
'''

# def meeting_requirement



