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

first_names_present = ['Adityaa', 'Aditya', 'Jai']
last_names_present = ['Adhikari', 'Agrawal', 'Agrawal']

first_names_hours = ['Adityaa', 'Aditya', 'Jai']
last_names_hours = ['Adhikari', 'Agrawal', 'Agrawal']

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


#
# def set_hours():
#
#

def get_hours(first_names, last_names):
    for index, name in enumerate(first_names):
        for list in list_of_lists:
            if name == list[1] and last_names[index] == list[0]:
                cell = sheet.find(name)
                sheet.update_cell(cell.row, 1, "Y")


# def get_least_active
''' Have to check number of hours, 0 1 or 2 events, 
'''

# def meeting_requirement



