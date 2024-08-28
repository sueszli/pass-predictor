"""
none of these functions are used - they are just here for reference
"""

import asyncio
import datetime
import functools
from typing import Optional

import bs4

from main import fetch, fetch_async


def get_course_groups(course_id: int) -> dict:
    # {group_id: group_name} ie. Mi14a, Mi14b, ...
    req = {
        "wsfunction": "core_group_get_course_groups",
        "courseid": course_id,
    }
    res = fetch(req)
    res = {elem["id"]: elem["name"] for elem in res}
    return res


def get_course_groupings(course_id: int) -> dict:
    # k1, k2
    # each group is in a grouping
    req = {
        "wsfunction": "core_group_get_course_groupings",
        "courseid": course_id,
    }
    res = fetch(req)
    res = {elem["id"]: elem["name"] for elem in res}
    return res


def get_course_assignments(course_id: int) -> dict:
    # all assignment fields
    # (name, id, grade)

    req = {
        "wsfunction": "mod_assign_get_assignments",
        "courseids[0]": course_id,
    }
    res = fetch(req)["courses"][0]["assignments"]
    res = [
        {
            "id": elem["id"],
            "cmid": elem["cmid"],
            "name": elem["name"],
            "grade": elem["grade"],
        }
        for elem in res
    ]
    return res


def get_course_quizzes(course_id: int) -> dict:
    # all online tuwel quizzes
    # (name, id)

    req = {
        "wsfunction": "mod_quiz_get_quizzes_by_courses",
        "courseids[0]": course_id,
    }
    res = fetch(req)["quizzes"]
    res = [
        {
            "id": elem["id"],
            "coursemodule": elem["coursemodule"],
            "name": elem["name"],
        }
        for elem in res
    ]

    return res


def get_course_grade_items(course_id: int) -> dict:
    # all submissions
    # {category: [{name, id}]}

    req = {
        "wsfunction": "core_grades_get_gradeitems",
        "courseid": course_id,
    }
    res = fetch(req)["gradeItems"]

    # merge by "category"
    res = functools.reduce(lambda acc, elem: acc.update({elem["category"]: acc.get(elem["category"], []) + [elem]}) or acc, res, {})
    for key in res:
        for elem in res[key]:
            elem.pop("category", None)

    return res


async def get_student_assignment_submissions(course_id, user_id: int) -> dict:
    # this is just a subset of `gradereport_user_get_grade_items`
    # but the number of `submitted` assignments could be useful

    def _get_course_assignments(course_id: int) -> dict:
        # (name, id, grade)
        req = {
            "wsfunction": "mod_assign_get_assignments",
            "courseids[0]": course_id,
        }
        res = fetch(req)["courses"][0]["assignments"]
        res = [
            {
                "id": elem["id"],
                "cmid": elem["cmid"],
                "name": elem["name"],
                "grade": elem["grade"],
            }
            for elem in res
        ]
        return res

    submissions = _get_course_assignments(course_id)

    async def _check_if_handed_in(assignment_id: int, assignment: dict) -> dict:
        req = {
            "wsfunction": "mod_assign_get_participant",
            "userid": user_id,
            "assignid": assignment_id,
        }
        res = await fetch_async(req)
        res.update(assignment)
        return res

    tasks = [_check_if_handed_in(a["id"], a) for a in submissions]
    results = await asyncio.gather(*tasks)
    results = [elem for elem in results if "exception" not in elem]
    results = [
        {
            "name": elem["name"],
            "id": elem["id"],
            "cmid": elem["cmid"],
            "submitted": elem["submitted"],
            "submissionstatus": elem["submissionstatus"],
            "requiregrading": elem["requiregrading"],
            "grade": elem["grade"],
        }
        for elem in results
    ]
    return results


def get_student_grades(course_id: int, user_id: int) -> dict:
    # `gradereport_user_get_grades_table` and `gradereport_user_get_grade_items` serve the same data - which renders
    # the group_id doesn't change anything, so get the first one of student
    def _get_random_group_id(course_id: int, user_id: int) -> int:
        req = {
            "wsfunction": "core_user_get_course_user_profiles",
            "userlist[0][userid]": user_id,
            "userlist[0][courseid]": course_id,
        }
        res = fetch(req)[0]
        if "groups" in res and len(res["groups"]) > 0:
            groups = [elem["id"] for elem in res["groups"]]
            return int(groups[0])
        else:
            return -1

    group_id = _get_random_group_id(course_id, user_id)
    if group_id == -1:
        return {}

    req = {
        "wsfunction": "gradereport_user_get_grades_table",
        "courseid": course_id,
        "userid": user_id,
        "groupid": group_id,
    }
    res = fetch(req)["tables"][0]["tabledata"]

    # parse html
    res = [elem for elem in res if "leader" not in elem]
    for elem in res:
        if "itemname" in elem:
            elem["itemname"] = elem["itemname"]["content"]
            elem["itemname"] = bs4.BeautifulSoup(elem["itemname"], "html.parser").text
            elem["itemname"] = elem["itemname"].replace("\n", "")
        if "weight" in elem:
            elem["weight"] = elem["weight"]["content"]
        if "grade" in elem:
            elem["grade"] = elem["grade"]["content"]
        if "range" in elem:
            elem["range"] = elem["range"]["content"]
        if "feedback" in elem:
            elem["feedback"] = elem["feedback"]["content"]
        if "contributiontocoursetotal" in elem:
            elem["contributiontocoursetotal"] = elem["contributiontocoursetotal"]["content"]
        elem.pop("parentcategories", None)

    return res


def approx_age(matrikelnummer: str) -> Optional[int]:
    # based off of matriculation number specs by the austrian ministry of education
    # didn't work for the majority of the students

    matrikelnummer = "".join(filter(str.isdigit, str(matrikelnummer)))

    if len(matrikelnummer) < 8:
        return None

    year_digits = matrikelnummer[1:3]

    if int(year_digits) <= 99 and int(year_digits) >= 50:
        year = 1900 + int(year_digits)
    else:
        year = 2000 + int(year_digits)

    current_year = datetime.now().year
    approximate_age = current_year - year + 18
    return approximate_age
