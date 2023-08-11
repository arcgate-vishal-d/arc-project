import time
import webbrowser

from app.ArcSheet.auth import spreadsheet_service, client
from app.ArcSheet.auth import drive_service
from app.ArcSheet.arc_constants import BASE_URL, MASTER_EMAIL
from app.ArcSheet.extractor import *
from app.ArcSheet.evaluator import *
from datetime import datetime, timedelta


def get_sheet_data(sheet_id):
    sheet_data = spreadsheet_service.spreadsheets().get(
        spreadsheetId=sheet_id,
        fields="sheets(data(rowData(values(userEnteredFormat,formattedValue))))"
    ).execute()

    effective_sheet_data = spreadsheet_service.spreadsheets().get(
        spreadsheetId=sheet_id,
        fields="sheets(data(rowData(values(effectiveFormat,formattedValue))))"
    ).execute()

    if row_data := extract_row_data(sheet_data):
        return format_sheet_data(row_data, effective_sheet_data, sheet_id)
    return {}


def format_sheet_data(row_data, effective_sheet_data, sheet_id):
    border_side_data = extract_borders_sides(row_data)
    text_formatting_data = extract_text_format(row_data)
    horizontal_alignment_data = extract_horizontal_alignment(
        extract_row_data(effective_sheet_data))
    color_data = extract_colors(row_data)
    value_data = extract_values(row_data)
    formula_data = extract_formulas(sheet_id)

    return_data = {
        "horizontal_alignment_data": horizontal_alignment_data,
        "border_side_data": border_side_data,
        "text_formatting_data": text_formatting_data,
        "color_data": color_data,
        "value_data": value_data,
        "formula_data": formula_data,
    }
    return remove_empty_trailing_entries(return_data)

def add_hours_minutes(timestamp):
    # Convert timestamp to datetime object
    dt = datetime.fromtimestamp(timestamp)
    
    # Add 5 hours and 30 minutes to the datetime object
    dt = dt + timedelta(hours=5, minutes=30)
    
    # Convert back to timestamp
    new_timestamp = dt.timestamp()
    
    return new_timestamp


def open_sheet(sheet_id):
    webbrowser.open(BASE_URL + sheet_id)  # Go to example.com


def create_sheet(username):
    spreadsheet_details = {
        'properties': {
            'title': f'{username} Sheet Test {time.time()}'   # Sheet name
        }
    }
    sheet = spreadsheet_service.spreadsheets().create(
        body=spreadsheet_details).execute()
    sheet_id = sheet.get('spreadsheetId')

    # share sheet to the master email
    master_permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': MASTER_EMAIL
    }
    drive_service.permissions().create(
        fileId=sheet_id, body=master_permission).execute()
    return sheet_id


def make_sheet_public(sheet_id):
    user_permission = {
        'type': 'anyone',
        'role': 'writer',
    }
    result = drive_service.permissions().create(
        fileId=sheet_id,
        body=user_permission,
        supportsTeamDrives=True,
    ).execute()


def make_sheet_private(sheet_id):
    result = drive_service.permissions().delete(
        fileId=sheet_id,
        permissionId='anyoneWithLink'
    ).execute()


def list_sheet_permissions(sheet_id):
    result = drive_service.permissions().list(
        fileId=sheet_id
    ).execute()


def remove_empty_trailing_entries(data_dict: dict):
    keys = data_dict.keys()
    for key in keys:
        for i in range(len(data_dict[key])-1, -1, -1):
            for j in range(len(data_dict[key][i])-1, -1, -1):
                if data_dict[key][i][j]:
                    break
                data_dict[key][i].pop()
        for i in range(len(data_dict[key])-1, -1, -1):
            if data_dict[key][i]:
                break
            data_dict[key].pop()

    return data_dict


def evaluate_results(hr_data: dict, examinee_data: dict):
    marks_map = entity_marks_map(hr_data)
    return sum(
        evaluate_marks(hr_data, examinee_data, key) for key in marks_map.keys()
    )

# sheet last edited time


def sheet_modified(sheet_id):
    sheet_data = drive_service.permissions().list(
        fileId=sheet_id).execute()
    fileId = sheet_id  # Please set spreadsheet ID.
    return (drive_service.files().get(fileId=fileId, fields="modifiedTime").execute())


# make list dict key should be entities that are present only pass those to evalute function
def entity_marks_map(hr_data: dict):
    dict_keys = hr_data.keys()
    format_data_list = list(dict_keys)
    entity = {}
    entity_list = []
    for keyset in format_data_list:
        if hr_data[keyset]:
            entity[keyset] = hr_data[keyset]
    entity_marks_map_dict = {
        'formula_data': 60,
    }
    for attr in entity:
        if attr != 'formula_data':
            entity_marks_map_dict[attr] = 40/(len(entity)-1)
    return entity_marks_map_dict


""" create candidate sheet only if it doesn't already exists"""
def create_candidate_sheet(username):
    from app.models import CandidateDetails
    user = CandidateDetails.objects.filter(id=username).first()
    if user.sheet_id is not None:
        return user.sheet_id
    sheet = True
    while sheet:
        spreadsheet_details = {
            'properties': {
                'title': f'{username} Sheet Test {time.time()}'   # Sheet name
            }
        }
        sheet = spreadsheet_service.spreadsheets().create(
            body=spreadsheet_details).execute()
        sheet_id = sheet.get('spreadsheetId')

        candidate = CandidateDetails.objects.filter(id=username).first()
        candidate.sheet_id = sheet_id

        if candidate.sheet_id:
            candidate.save()
            sheet = False
     # share sheet to the master email
    master_permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': MASTER_EMAIL
    }
    drive_service.permissions().create(
        fileId=sheet_id, body=master_permission).execute()
    return sheet_id
