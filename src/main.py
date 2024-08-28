import asyncio
import functools
import json
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional

import aiohttp
import yaml
from tqdm.asyncio import tqdm
from transformers import pipeline

"""
request utils
"""

configpath = Path.cwd() / "config.yml"
CONFIG: dict = yaml.safe_load(configpath.read_text())


def fetch(data: dict) -> dict:
    baseurl = "https://tuwel.tuwien.ac.at/webservice/rest/server.php"
    request_body = urllib.parse.urlencode(
        {
            "wstoken": CONFIG["key"],
            "moodlewsrestformat": "json",
            **data,
        }
    ).encode()
    response = urllib.request.urlopen(baseurl, request_body)
    response = json.loads(response.read().decode())
    return response


async def fetch_async(data: dict) -> dict:
    baseurl = "https://tuwel.tuwien.ac.at/webservice/rest/server.php"
    request_body = {
        "wstoken": CONFIG["key"],
        "moodlewsrestformat": "json",
        **data,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(baseurl, data=request_body) as response:
            assert response.status == 200, f"status code: {response.status}"
            return await response.json()


def print_json(data: dict) -> None:
    # prints umlaute correctly
    print(json.dumps(data, indent=4, ensure_ascii=False))


"""
ids
"""


def get_course_id(term: str) -> int:
    ep1 = "185A91"
    req = {
        "wsfunction": "core_course_get_courses_by_field",
        "field": "idnumber",
        "value": ep1 + "-" + term,
    }
    res = fetch(req)
    return res["courses"][0]["id"]


def get_student_ids(course_id) -> list[int]:
    req = {
        "wsfunction": "core_grades_get_gradable_users",
        "courseid": course_id,
    }
    res = fetch(req)["users"]
    ids = [elem["id"] for elem in res]
    return ids


"""
course stats
"""


def get_forum_participants(course_id: int) -> dict:
    def _get_forum_id():
        req = {
            "wsfunction": "mod_forum_get_forums_by_courses",
            "courseids[0]": course_id,
        }
        forum_id = fetch(req)[1]["id"]
        return forum_id

    def _get_participants(dis_id: int):
        req = {
            "wsfunction": "mod_forum_get_discussion_posts",
            "discussionid": dis_id,
        }
        participants = [elem["author"]["id"] for elem in fetch(req)["posts"]]
        return participants

    req = {
        "wsfunction": "mod_forum_get_forum_discussions",
        "forumid": _get_forum_id(),
    }
    res = fetch(req)["discussions"]
    res = [
        {
            "discussion": elem["discussion"],
            "author": elem["userid"],
            "participants": _get_participants(elem["discussion"]),
        }
        for elem in res
    ]
    return res


"""
student stats
"""


sex_classifier = pipeline("text-classification", model="padmajabfrl/Gender-Classification")


def get_sex(name: str) -> Optional[str]:
    cls = sex_classifier(name)[0]["label"]
    if cls not in ["Male", "Female"]:
        cls = None
    return cls


async def get_student_passed(course_id: int, user_id: int) -> bool:
    req = {
        "wsfunction": "gradereport_user_get_grade_items",
        "courseid": course_id,
        "userid": user_id,
    }
    res = await fetch_async(req)
    res = res["usergrades"][0]["gradeitems"]
    res = [
        {
            "id": elem["id"],
            "itemname": elem["itemname"],
            "itemmodule": elem["itemmodule"],
            "idnumber": elem["idnumber"],
            "graderaw": elem["graderaw"],
            "grademin": elem["grademin"],
            "grademax": elem["grademax"],
            "gradeformatted": elem["gradeformatted"],
        }
        for elem in res
    ]

    # merge by "itemmodule"
    res = functools.reduce(lambda acc, elem: acc.update({elem["itemmodule"]: acc.get(elem["itemmodule"], []) + [elem]}) or acc, res, {})
    for key in res:
        for elem in res[key]:
            elem.pop("itemmodule", None)
    res["unknown"] = res.pop(None, [])

    # check if passed
    res = res["unknown"][-1]["gradeformatted"]
    passed = not any([s in res for s in ["(-)", "(N5)"]])
    return passed


async def get_student_enrolled_courses(user_id: int) -> dict:
    req = {
        "wsfunction": "core_enrol_get_users_courses",
        "userid": user_id,
    }
    res = await fetch_async(req)
    res = [
        {
            "id": elem["id"],
            "idnumber": elem["idnumber"],
            "fullname": elem["fullname"],
            "enrolledusercount": elem["enrolledusercount"],
            "enablecompletion": elem["enablecompletion"],
            "completionhascriteria": elem["completionhascriteria"],
            "completionusertracked": elem["completionusertracked"],
            "progress": elem["progress"],
            "completed": elem["completed"],
            "startdate": elem["startdate"],
            "enddate": elem["enddate"],
            "marker": elem["marker"],
            "lastaccess": elem["lastaccess"],
        }
        for elem in res
    ]
    return res


async def get_student_grades(course_id: int, user_id: int) -> dict:
    req = {
        "wsfunction": "gradereport_user_get_grade_items",
        "courseid": course_id,
        "userid": user_id,
    }
    res = await fetch_async(req)
    res = res["usergrades"][0]["gradeitems"]
    res = [
        {
            "id": elem["id"],
            "itemname": elem["itemname"],
            "itemmodule": elem["itemmodule"],
            "idnumber": elem["idnumber"],
            "graderaw": elem["graderaw"],
            "grademin": elem["grademin"],
            "grademax": elem["grademax"],
            "gradeformatted": elem["gradeformatted"],
        }
        for elem in res
    ]

    # merge by "itemmodule"
    res = functools.reduce(lambda acc, elem: acc.update({elem["itemmodule"]: acc.get(elem["itemmodule"], []) + [elem]}) or acc, res, {})
    for key in res:
        for elem in res[key]:
            elem.pop("itemmodule", None)
    res["unknown"] = res.pop(None, [])
    return res


async def get_student_stats(course_id: int, user_id: int) -> dict:
    req = {
        "wsfunction": "core_user_get_course_user_profiles",
        "userlist[0][userid]": user_id,
        "userlist[0][courseid]": course_id,
    }
    res = await fetch_async(req)
    res = res[0]

    res["sex"] = get_sex(res["fullname"])
    res["passed"] = await get_student_passed(course_id, user_id)
    res["enrolled_courses"] = await get_student_enrolled_courses(user_id)
    res["grades"] = await get_student_grades(course_id, user_id)

    res.pop("roles", None)
    res.pop("country", None)
    res.pop("city", None)
    res.pop("firstname", None)
    res.pop("lastname", None)
    res.pop("fullname", None)
    res.pop("lastaccess", None)
    res.pop("email", None)
    res.pop("profileimageurlsmall", None)
    res.pop("profileimageurl", None)
    res.pop("timezone", None)
    res.pop("suspended", None)
    res.pop("description", None)
    res.pop("descriptionformat", None)
    res.pop("enrolledcourses", None)

    async def _get_course_groups(course_id: int) -> dict:
        # {group_id: group_name} ie. Mi14a, Mi14b, ...
        req = {
            "wsfunction": "core_group_get_course_groups",
            "courseid": course_id,
        }
        res = await fetch_async(req)
        res = {elem["id"]: elem["name"] for elem in res}
        return res

    course_groups = await _get_course_groups(course_id)

    if "groups" in res:
        res["groups"] = [elem["id"] for elem in res["groups"]]
        res["groups"] = {elem: course_groups.get(elem, "unknown") for elem in res["groups"]}
    return res


"""
main loop
"""


def get_result(course_id: int, user_id: int) -> dict:
    student = get_student_stats(course_id, user_id)

    forum_participants = get_forum_participants(course_id)
    student["forum_stats"] = {
        "authorship_count": len([elem for elem in forum_participants if elem["author"] == user_id]),
        "participation_count": len([elem for elem in forum_participants if user_id in elem["participants"]]),
    }
    return student


async def main():
    terms = ["2017W", "2018S", "2018W", "2019S", "2019W", "2020S", "2020W", "2021S", "2021W", "2022S", "2022W", "2023S", "2023W", "2024S"]

    for term in terms:
        course_id = get_course_id(term)

        uids = get_student_ids(course_id)

        tasks = [get_student_stats(course_id, uid) for uid in uids]
        results = await tqdm.gather(*tasks, total=len(uids), desc=f"{term} term")

        outpath = Path.cwd() / f"{term}.json"
        with open(outpath, "w") as f:
            json.dump(results, f, indent=4, ensure_ascii=True)


if __name__ == "__main__":
    asyncio.run(main())
