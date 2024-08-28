import datetime
import glob
import json
from pathlib import Path


def _strip_strings(data: dict) -> dict:
    new_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            new_data[key] = _strip_strings(value)
        elif isinstance(value, list):
            new_data[key] = [_strip_strings(item) for item in value]
        elif isinstance(value, str):
            new_data[key] = value.strip()
        else:
            new_data[key] = value
    return new_data


def _drop_ids(data: dict, depth: int = 0) -> dict:
    new_data = {}
    for key, value in data.items():
        if key == "id":
            continue
        if isinstance(value, dict):
            new_data[key] = _drop_ids(value, depth + 1)
        elif isinstance(value, list):
            new_data[key] = [_drop_ids(item, depth + 1) for item in value]
        else:
            new_data[key] = value
    return new_data


def _get_enrollment_year(matriculation_number: str) -> int:
    if ";" in matriculation_number:
        matriculation_number = matriculation_number.split(";")[0]

    matriculation_number = matriculation_number.strip()
    length = len(matriculation_number)

    assert length == 7 or length == 8
    if length == 8:
        year_digits = matriculation_number[1:3]
    elif length == 7:
        year_digits = matriculation_number[0:2]

    current_year = int(str(2024)[2:])  # get the last two digits of the current year
    enrollment_year = int(year_digits)

    # assume the year is in the past or current year
    if enrollment_year > current_year:
        enrollment_year += 1900
    else:
        enrollment_year += 2000

    return enrollment_year


def _fix_courses(term: str, student: dict) -> dict:
    student = student.copy()

    def _get_time_label(current_term: str, startdate: int) -> str:  # "before", "after", "current"
        curr_year = int(current_term[:4])
        curr_sem = current_term[4]  # S or W

        startdate = datetime.datetime.fromtimestamp(startdate)
        other_year = startdate.year
        other_month = startdate.month
        other_sem = "S" if 3 <= other_month <= 9 else "W"

        if other_year < curr_year or (other_year == curr_year and other_sem == "S" and curr_sem == "W"):
            return "before"
        elif other_year > curr_year or (other_year == curr_year and other_sem == "W" and curr_sem == "S"):
            return "after"
        else:
            return "current"

    courses = student["enrolled_courses"]
    for course in courses:
        course.pop("completionhascriteria")  # always false
        course.pop("completionusertracked")  # always false
        course.pop("completed")  # always false
        course.pop("enddate")  # missing for far too many courses
        course.pop("marker")  # not sure what it means

        course["time_label"] = _get_time_label(term, course["startdate"])

    # drop if ep1
    ep1id = "185A91"
    for course in courses:
        if ep1id in course["idnumber"]:
            courses.remove(course)

    # drop all courses that are current (i.e. the term is the same as the term of the course)
    # we can discard older courses because tuwel doesn't store them
    student["current_courses"] = [course for course in courses if course["time_label"] == "current"]
    student.pop("enrolled_courses")
    for course in student["current_courses"]:
        course.pop("time_label")
    return student


def _fix_grades(student: dict) -> dict:
    student = student.copy()

    def flatten_grades(grades):
        return [{**item, "type": grade_type} for grade_type, items in grades.items() for item in items]

    if "grades" in student:
        student["grades"] = flatten_grades(student["grades"])

    # fix html output
    for grade in student["grades"]:
        if "gradeformatted" in grade and len(grade["gradeformatted"]) > 20:
            grade["gradeformatted"] = grade["gradeformatted"].split("</i>")[1]

    # aggregate points, throw away the rest
    student["points_quiz"] = 0
    student["points_assign"] = 0
    student["points_checkmark"] = 0
    student["points_organizer"] = 0
    student["points_unknown"] = 0
    student["points_total"] = 0
    for grade in student["grades"]:
        gradetype = grade["type"]
        if gradetype not in ["quiz", "assign", "checkmark", "organizer", "unknown"]:
            continue
        if "graderaw" in grade and grade["graderaw"] is not None:
            student[f"points_{gradetype}"] += grade["graderaw"]
            student["points_total"] += grade["graderaw"]

    # drop grades
    student.pop("grades")

    # drop points_organizer as it is always 0
    student.pop("points_organizer")
    return student


def _process_student(term: str, student: dict) -> dict:
    out = student.copy()

    only_keys = ["id", "idnumber", "firstaccess", "sex", "passed", "enrolled_courses", "grades"]
    out = {key: value for key, value in out.items() if key in only_keys}

    term_year = int(term[0:4])

    out.pop("firstaccess")
    out["years_enrolled"] = term_year - _get_enrollment_year(student["idnumber"])
    out.pop("idnumber")

    out = _strip_strings(out)
    out = _drop_ids(out)
    out = _fix_courses(term, out)
    out = _fix_grades(out)

    return out


"""
public functions
"""


def print_json(data: dict) -> None:
    print(json.dumps(data, indent=4, ensure_ascii=False))


def print_keys(d, indent=0) -> None:
    for k, v in d.items():
        print("\t" * indent + k + f" [{type(v).__name__}]")
        if isinstance(v, dict):
            print_keys(v, indent + 1)
        elif isinstance(v, list):
            if len(v) > 0:
                print_keys(v[0], indent + 1)


TERMS = ["2017W", "2018S", "2018W", "2019S", "2019W", "2020S", "2020W", "2021S", "2021W", "2022S", "2022W", "2023S", "2023W", "2024S"]


def get_term(term: str) -> dict:
    assert term in TERMS, f"invalid term: {term}"

    datapath = Path(__file__).parent.parent / "data"
    filepaths = glob.glob(str(datapath / "*.json"))
    assert all(Path(filepath).exists() for filepath in filepaths)
    data = json.loads((datapath / f"{term}.json").read_text())

    required_keys = ["id", "idnumber", "firstaccess", "sex", "passed", "enrolled_courses", "grades"]
    processed_data = [
        _process_student(term, student)
        for student in data
        if all(key in student for key in required_keys)  # drops 5 students
    ]

    return processed_data


# for term in TERMS:
#     print(term)
#     for student in get_term(term):
#         print_json(student)
#         # print_keys(student)
