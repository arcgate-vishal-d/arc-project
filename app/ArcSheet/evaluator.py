from app.ArcSheet.arc_constants import MAX_FORMULA_MARKS, MAX_BORDER_MARKS, MAX_COLOR_MARKS, \
    MAX_FORMATTING_MARKS, MAX_HORIZONTAL_ALIGNMENT_MARKS, MAX_VALUE_MARKS


def evaluate_marks(hr_data, examinee_data, entity):
    # import inside function to escape circular loop
    entity_hr_data = hr_data.get(entity, {})
    entity_examinee_data = examinee_data.get(entity, {})
    marks_per_cell = get_marks_per_cell(hr_data, entity)
    num_common_elements = 0
    for sublist1, sublist2 in zip(entity_hr_data, entity_examinee_data):
        for elem1, elem2 in zip(sublist1, sublist2):
            if elem1 == elem2 and elem1 != "":
                num_common_elements += 1

    # deduct marks of extra entries are given
    examinee_length = get_total_entries(entity_examinee_data)
    hr_length = get_total_entries(entity_hr_data)
    if examinee_length > hr_length:
        num_common_elements = num_common_elements - \
            (examinee_length - hr_length)
    num_common_elements = max(num_common_elements, 0)
    return num_common_elements*marks_per_cell

def get_marks_per_cell(hr_data, entity):
    from app.ArcSheet import base_view
    entity_hr_data = hr_data.get(entity)
    
    empty_entries = get_empty_entries(entity_hr_data)
    total_entries = get_total_entries(entity_hr_data)
    actual_entries = total_entries - empty_entries
    return base_view.entity_marks_map(hr_data).get(entity)/actual_entries


def get_empty_entries(hr_data):
    return sum(i.count('') for i in hr_data)


def get_total_entries(hr_data):
    return sum(len(x) for x in hr_data)
