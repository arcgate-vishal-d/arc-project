from app.ArcSheet.arc_constants import TEXT_FORMATS, HORIZONTAL_ALIGNMENTS
from app.ArcSheet.auth import spreadsheet_service


def extract_borders_sides(row_data):
    border_side_data = []
    for row in row_data:
        if row:
            border_side_data.append([])
            for column in row.get("values"):
                border_side_data[-1].append(
                    list(column.get("userEnteredFormat", {}).get("borders", {}).keys()))

    return border_side_data


def extract_text_format(row_data):
    text_format_data = []
    for row in row_data:
        if row:
            text_format_data.append([])
            for column in row.get("values"):
                if column.get("formattedValue"):
                    data = list(column.get("userEnteredFormat",
                                {}).get("textFormat", {}).keys())
                    data = [(i) for i in data if i in TEXT_FORMATS]
                    text_format_data[-1].append(data)

    return text_format_data


def extract_horizontal_alignment(effective_sheet_data):
    text_format_data = []
    for row in effective_sheet_data:
        if row:
            text_format_data.append([])
            for column in row.get("values"):
                if column.get("formattedValue"):
                    data = column.get("effectiveFormat",
                                      {}).get("horizontalAlignment", '').strip().lower()
                    data = data if data in HORIZONTAL_ALIGNMENTS else ''
                    text_format_data[-1].append(data)
    return text_format_data


def extract_values(row_data):
    value_data = []
    for row in row_data:
        if row:
            value_data.append([])
            for column in row.get("values"):
                data = column.get("formattedValue", '')
                value_data[-1].append(data.lower().strip().replace(" ", ""))
    return value_data


def extract_colors(row_data):
    colors_data = []
    for row in row_data:
        if row:
            colors_data.append([])
            for column in row.get("values"):
                colors_data[-1].append(column.get("userEnteredFormat",
                                                  {}).get("backgroundColor", ''))
    return colors_data


def extract_formulas(sheet_id):
    formula_data = spreadsheet_service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range='A1:Z1000', valueRenderOption='FORMULA').execute().get('values')
    if not formula_data:
        return []
    for i in range(len(formula_data)):
        for j in range(len(formula_data[i])):
            if not str(formula_data[i][j]).startswith('='):
                formula_data[i][j] = ''
    return formula_data


def extract_row_data(sheet_data):
    return sheet_data.get('sheets', [{}])[0].get('data', [{}])[0].get('rowData')
