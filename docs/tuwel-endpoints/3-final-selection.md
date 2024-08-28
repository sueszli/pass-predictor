> these endpoints are safe and relevant
> 
> to find additional endpoints see: https://tuwel.tuwien.ac.at/webservice/wsdoc.php?id=10151

student-course relationship:

- `core_grades_get_gradable_users` ✅ (use instead of `core_enrol_get_enrolled_users` to avoid fetching tutors)
- `core_enrol_get_enrolled_users` ✅
- `core_user_get_course_user_profiles` ✅
- `core_enrol_get_users_courses` ✅

course content:

- `core_course_get_courses` (redundant, course metadata)
- `core_course_get_contents` (course html content)
- `mod_resource_get_resources_by_courses` (course html content)
- `core_course_get_courses_by_field`

student groups:

- `core_group_get_course_groups` ✅
- `core_group_get_course_user_groups` (redundant, `core_grades_get_gradable_users` already fetches this)
- `core_group_get_course_groupings` ✅

grades:

- `gradereport_user_get_grade_items` ✅
- `core_grades_get_gradeitems` ✅
- `gradereport_user_get_grades_table` (redundant, `gradereport_user_get_grade_items` already fetches this)

quizzes:

- `mod_quiz_get_quizzes_by_courses` ✅
- `mod_quiz_get_user_attempts` (just returns "attempts" and "warnings" as strings, no ids)
- `mod_quiz_get_attempt_review` (there is no way to access attempt ids, which are needed for this endpoint)
- `mod_quiz_get_attempt_access_information`
- `mod_quiz_get_user_best_grade`
- `mod_quiz_get_attempt_data`
- `mod_quiz_get_attempt_summary`
- `mod_quiz_get_combined_review_options`
- `mod_quiz_get_quiz_access_information`
- `mod_quiz_get_quiz_feedback_for_grade`
- `mod_quiz_get_quiz_required_qtypes`

assignments:

- `mod_assign_get_assignments` ✅
- `mod_assign_get_participant` ✅
- `mod_assign_get_submission_status` (system error)
- `mod_assign_list_participants` (not sure what this is good for, returns users, not assignments)
- `mod_assign_get_grades`
- `mod_assign_get_submissions`
- `mod_assign_get_user_flags`
- `mod_assign_get_user_mappings`
- `mod_assign_reveal_identities`

forum discussion:

- `mod_forum_get_forums_by_courses` ✅
- `mod_forum_get_discussion_posts` ✅
- `mod_forum_get_forum_discussions` ✅
- `core_comment_get_comments` (too detailed)
