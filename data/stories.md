## story 01
* acquaintance
    - action_acquaintance

## story 02
* greet
    - utter_greet

## story 03
* how_are_you
    - utter_how_are_you

## story 04 
* nice_to_meet_you
    - utter_nice_to_meet_you

# story 08
* inform_contact
    - action_contact

## story 09 
* goodbye
    - utter_goodbye

#story 8522
* acquaintance
    - action_acquaintance

## Generated Story 8362015419805915240
* inform_internship
    - action_internship
    - internship_form
    - form{"name": "internship_form"}
    - form{"name": null}
    - slot{"requested_slot": null}
* inform_internship{"internshipRef": "Ref-12188"}
    - slot{"internshipRef": "Ref-12188"}
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}

## apply happy path
* apply_job
    - apply_form
    - form{"name": "apply_form"}
    - form{"name": null}
    - utter_apply_slots_values

## Generated Story 4928413376213491340
* apply_job
    - apply_form
    - form{"name": "apply_form"}
    - slot{"requested_slot": "jobRef"}
* form: inform_apply{"jobRef": "job-39995"}
    - slot{"jobRef": "job-39995"}
    - form: apply_form
    - slot{"jobRef": "job-39995"}
    - slot{"requested_slot": "name"}
* form: inform_apply{"name": "Mohamed Karim"}
    - slot{"name": "Mohamed Karim"}
    - form: apply_form
    - slot{"name": "Mezghani Islem"}
    - slot{"requested_slot": "experience_years"}
* form: inform_apply{"experience_years": "2"}
    - slot{"experience_years": "2"}
    - form: apply_form
    - slot{"experience_years": "2"}
    - slot{"requested_slot": "phone_number"}
* form: inform_apply{"phone_number": "41155241"}
    - slot{"phone_number": "50730571"}
    - form: apply_form
    - slot{"phone_number": "50730571"}
    - slot{"requested_slot": "email"}
* form: inform_apply{"email": "islem@email.com"}
    - slot{"email": "islem@email.com"}
    - form: apply_form
    - slot{"email": "islem@email.com"}
    - slot{"requested_slot": "cv_link"}
* form: inform_apply{"cv_link": "linkedin.com/in/islem-mezghani-1a4369144/"}
    - slot{"cv_link": "linkedin.com/in/islem-mezghani-1a4369144/"}
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}

## Generated Story -870223808643095922
* inform_job
    - utter_ask_role
* inform_job{"role": "Software Development"}
    - slot{"role": "Software Development"}
    - action_sub_role
* inform_job{"sub_role": "Fullstack"}
    - slot{"sub_role": "Fullstack"}
    - action_job
    - slot{"jobRef": null}
* inform_apply{"jobRef": "job-83737"}
    - slot{"jobRef": "job-83737"}
    - utter_ask_apply
* affirm 
    - apply_form
    - action_store_applicant
    - action_deactivate_form
    - form{"name": null}
    - slot{"requested_slot": null}

## Generated Story -870223808643095922
* inform_job
    - utter_ask_role
* inform_job
    - action_sub_role
    - action_job
* inform_apply
    - utter_ask_apply
* deny 
    - utter_ask_detail
* ask_detail
    - action_show_details

##details story
* ask_detail
    - action_show_details

## Generated Story 5850874494677902334
* inform_job
    - utter_ask_role
* inform_job{"role": "Network and Security"}
    - slot{"role": "Network and Security"}
    - action_sub_role
* inform_job{"sub_role": "Network Speciality"}
    - slot{"sub_role": "Network Speciality"}
    - action_job
    - slot{"jobRef": "job-12128"}

## Generated Story 4342554994561008248
* inform_contact
    - action_contact

