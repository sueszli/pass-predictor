> these endpoints are safe but not relevant

# redundant

syntactic sugar:

- `tool_moodlenet_search_courses` - use `core_course_get_courses_by_field` instead
- `core_course_search_courses` - use `core_course_get_courses_by_field` instead
- `gradereport_grader_get_users_in_report` - use `core_grades_get_gradable_users` instead
- `mod_forum_get_discussion_post` - use `mod_forum_get_discussion_posts` instead

search functions:

- `core_search_get_results` - also has user id search
- `core_search_get_search_areas_list` - category only search
- `core_search_get_top_results` - ???
- `core_filters_get_available_in_context` - ???
- `core_user_get_users_by_field` - search for student in course
- `core_enrol_search_users` - search for student in course

# deprecated

deprecated:

- `core_grades_get_enrolled_users_for_search_widget`
- `core_grades_get_groups_for_search_widget`
- `mod_forum_get_forum_discussions_paginated`
- `core_grades_get_groups_for_selector`
- `core_grades_get_enrolled_users_for_selector`

breaks:

- `gradereport_singleview_get_grade_items_for_search_widget`
- `mod_checkmark_get_checkmarks_by_courses`
- `mod_checkmark_get_checkmark`
- `gradereport_overview_get_course_grades` (not permitted - also includes grades from other courses)

# not relevant

metadata:

- `core_webservice_get_site_info`

enrollment:

- `enrol_guest_get_instance_info`
- `enrol_self_get_instance_info`

notes:

- `core_notes_get_course_notes` (empty response)

completion status:

- `core_completion_get_activities_completion_status` (empty response)
- `core_completion_get_course_completion_status` (backend throws exception)

course content:

- `mod_label_get_labels_by_courses`
- `mod_folder_get_folders_by_courses`
- `core_files_get_files`
- `mod_url_get_urls_by_courses`
- `core_table_get_dynamic_table_content`
- `core_block_fetch_addable_blocks`
- `core_block_get_course_blocks`
- `core_course_get_categories`
- `core_course_get_course_module`
- `core_course_get_course_module_by_instance`
- `mod_book_get_books_by_courses`
- `mod_page_get_pages_by_coursess`
- `core_tag_get_tag_areas`
- `core_tag_get_tag_cloud`
- `core_tag_get_tag_collections`
- `core_tag_get_tagindex`
- `core_tag_get_tagindex_per_area`
- `mod_lesson_get_lesson`
- `mod_lesson_get_lesson_access_information`
- `mod_lesson_get_page_data`
- `mod_lesson_get_pages`
- `mod_lesson_get_pages_possible_jumps`

calendar views:

- `core_calendar_get_calendar_day_view`
- `core_calendar_get_calendar_event_by_id`
- `core_calendar_get_calendar_events`
- `core_calendar_get_calendar_monthly_view`
- `core_calendar_get_calendar_upcoming_view`

admin config:

- `tool_mobile_get_autologin_key`
- `tool_mobile_get_config`
- `tool_mobile_get_content`
- `tool_mobile_get_plugins_supporting_mobile`
- `tool_mobile_get_public_config`
- `tool_mobile_get_tokens_for_qr_login`
- `tool_mobile_validate_subscription_key`
- `tool_moodlenet_verify_webfinger`
- `enrol_guest_validate_password`
- `core_get_component_strings`

user privileges:

- `core_enrol_get_course_enrolment_methods`
- `core_course_get_user_administration_options`
- `core_course_get_user_navigation_options`
- `core_group_get_activity_allowed_groups`
- `core_group_get_activity_groupmode`
- `core_group_get_groups_for_selector`
- `core_calendar_get_allowed_event_types`
- `core_calendar_get_calendar_access_information`
- `tool_analytics_potential_contexts`
- `mod_forum_get_forum_access_information`
- `core_calendar_get_calendar_export_token`
- `gradereport_user_get_access_information`

reportbuilder:

- `core_reportbuilder_list_reports`
- `core_reportbuilder_retrieve_report`
- `core_reportbuilder_retrieve_system_report`

rating:

- `core_rating_get_item_ratings`

# unused features

scorm (self-contained object):

- `mod_scorm_get_scorm_access_information`
- `mod_scorm_get_scorm_attempt_count`
- `mod_scorm_get_scorm_sco_tracks`
- `mod_scorm_get_scorm_scoes`
- `mod_scorm_get_scorm_user_data`
- `mod_scorm_get_scorms_by_courses`

lessons:

- `mod_lesson_get_lessons_by_courses`
- `mod_lesson_get_attempts_overview`
- `mod_lesson_get_questions_attempts`
- `mod_lesson_get_user_attempt`
- `mod_lesson_get_user_attempt_grade`
- `mod_lesson_get_user_grade`
- `mod_lesson_get_user_timers`

surveys / choices / feedback:

- `mod_survey_get_questions`
- `mod_survey_get_surveys_by_courses`
- `mod_choice_get_choice_options`
- `mod_choice_get_choice_results`
- `mod_choice_get_choices_by_courses`
- `mod_feedback_get_analysis`
- `mod_feedback_get_current_completed_tmp`
- `mod_feedback_get_feedback_access_information`
- `mod_feedback_get_feedbacks_by_courses`
- `mod_feedback_get_finished_responses`
- `mod_feedback_get_items`
- `mod_feedback_get_last_completed`
- `mod_feedback_get_non_respondents`
- `mod_feedback_get_page_items`
- `mod_feedback_get_responses_analysis`
- `mod_feedback_get_unfinished_responses`

calendar action events:

- `core_calendar_get_action_events_by_course`
- `core_calendar_get_action_events_by_courses`
- `core_calendar_get_action_events_by_timesort`
- `core_course_get_enrolled_courses_with_action_events_by_timeline_classification`
- `core_course_get_enrolled_courses_by_timeline_classification`
- `core_course_get_updates_since`
- `core_course_check_updates`

user badges:

- `core_badges_get_user_badge_by_hash`
- `core_badges_get_user_badges`

big-blue-button videochat:

- `mod_bigbluebuttonbn_can_join`
- `mod_bigbluebuttonbn_get_bigbluebuttonbns_by_courses`
- `mod_bigbluebuttonbn_get_join_url`
- `mod_bigbluebuttonbn_get_recordings`
- `mod_bigbluebuttonbn_get_recordings_to_import`
- `mod_bigbluebuttonbn_meeting_info`

wiki:

- `mod_wiki_get_page_contents`
- `mod_wiki_get_page_for_editing`
- `mod_wiki_get_subwiki_files`
- `mod_wiki_get_subwiki_pages`
- `mod_wiki_get_subwikis`
- `mod_wiki_get_wikis_by_courses`

h5p:

- `core_h5p_get_trusted_h5p_file`
- `mod_h5pactivity_get_attempts`
- `mod_h5pactivity_get_h5pactivities_by_courses`
- `mod_h5pactivity_get_h5pactivity_access_information`
- `mod_h5pactivity_get_results`
- `mod_h5pactivity_get_user_attempts`

blogs:

- `core_blog_get_entries`

imscp:

- `mod_imscp_get_imscps_by_courses`

external tools:

- `mod_lti_get_ltis_by_courses`
- `mod_lti_get_tool_launch_data`

xapi:

- `core_xapi_get_state`
- `core_xapi_get_states`

database activity:

- `mod_data_get_data_access_information`
- `mod_data_get_databases_by_courses`
- `mod_data_get_entries`
- `mod_data_get_entry`
- `mod_data_get_fields`
- `mod_data_search_entries`

glossary:

- `mod_glossary_get_authors`
- `mod_glossary_get_categories`
- `mod_glossary_get_entries_by_author`
- `mod_glossary_get_entries_by_author_id`
- `mod_glossary_get_entries_by_category`
- `mod_glossary_get_entries_by_date`
- `mod_glossary_get_entries_by_letter`
- `mod_glossary_get_entries_by_search`
- `mod_glossary_get_entries_by_term`
- `mod_glossary_get_entries_to_approve`
- `mod_glossary_get_entry_by_id`
- `mod_glossary_get_glossaries_by_courses`

workshop:

- `mod_workshop_get_assessment`
- `mod_workshop_get_assessment_form_definition`
- `mod_workshop_get_grades`
- `mod_workshop_get_grades_report`
- `mod_workshop_get_reviewer_assessments`
- `mod_workshop_get_submission`
- `mod_workshop_get_submission_assessments`
- `mod_workshop_get_submissions`
- `mod_workshop_get_user_plan`
- `mod_workshop_get_workshop_access_information`
- `mod_workshop_get_workshops_by_courses`

course competency / learning plans:

- `core_competency_get_scale_values`
- `core_competency_list_course_competencies`
- `tool_lp_data_for_course_competencies_page`
- `tool_lp_data_for_user_competency_summary`
- `tool_lp_data_for_user_competency_summary_in_course`
- `tool_lp_data_for_user_competency_summary_in_plan`
- `tool_lp_data_for_user_evidence_list_page`
- `tool_lp_data_for_user_evidence_page`
- `tool_lp_data_for_plan_page`
- `tool_lp_data_for_plans_page`

# not accessible

private files (mostly used by lecturers):

- `core_user_get_private_files_info`

recent clicks (no permission to access):

- `core_course_get_recent_courses`
- `block_recentlyaccesseditems_get_recent_items`

preferences (no permission to access):

- `core_block_get_dashboard_blocks`
- `block_starredcourses_get_starred_courses`
- `core_user_get_user_preferences`
- `message_airnotifier_are_notification_preferences_configured`
- `message_airnotifier_get_user_devices`
- `message_airnotifier_is_system_configured`
- `message_popup_get_popup_notifications`
- `message_popup_get_unread_popup_notification_count`

chat messages (no permission to access):

- `core_message_data_for_messagearea_search_messages`
- `core_message_get_blocked_users`
- `core_message_get_contact_requests`
- `core_message_get_conversation`
- `core_message_get_conversation_between_users`
- `core_message_get_conversation_counts`
- `core_message_get_conversation_members`
- `core_message_get_conversation_messages`
- `core_message_get_conversations`
- `core_message_get_member_info`
- `core_message_get_messages`
- `core_message_get_received_contact_requests_count`
- `core_message_get_self_conversation`
- `core_message_get_unread_conversation_counts`
- `core_message_get_unread_conversations_count`
- `core_message_get_unread_notification_count`
- `core_message_get_user_contacts`
- `core_message_get_user_message_preferences`
- `core_message_get_user_notification_preferences`
- `core_message_message_search_users`
- `core_message_search_contacts`
- `mod_chat_get_chat_latest_messages`
- `mod_chat_get_chat_users`
- `mod_chat_get_chats_by_courses`
- `mod_chat_get_session_messages`
- `mod_chat_get_sessions`
