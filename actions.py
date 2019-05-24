
# -*- coding: utf-8 -*-
from typing import Dict, Text, Any, List, Union, Optional
from rasa_core_sdk import Action
from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk import Tracker
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.executor import CollectingDispatcher
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT
import re
# Our packages
from repository.job_data import get_job_data, list_jobs, getRoleID ,generate_job_buttons
from repository.applicant_data import saveApplicantData 
from repository.internship_data import list_internships, generate_internship_buttons


# jobs action
class action_job(Action):
    def name(self):
        return "action_job"
    def run(self, dispatcher, tracker, domain):
        jobRef = tracker.get_slot("jobRef")
        user_id = (tracker.current_state())["sender_id"]
         #user_id = "189c6a81-abde-4388-a757-a50da959e8da"
        sub_role = (tracker.get_slot("sub_role"))
        role_id = getRoleID(sub_role)

            # creates a list out of the existing jobs.
        possible_jobs = list_jobs(user_id, role_id)
        if(possible_jobs):
            message = "These are the available positions that i know about!"
        else:
            message= " We don't have an open position in "+ sub_role+", please try again"
        # generates a list of buttons from the list of possible_jobs
        buttons = generate_job_buttons(possible_jobs)
        dispatcher.utter_button_message(message, buttons)
        return [SlotSet("jobRef", jobRef)]

class actionSubRole(Action):
    def name(self):
        return "action_sub_role"
    def run(self, dispatcher, tracker, domain ):
        role = tracker.get_slot("role")
        dev_sub_role_list=[{"payload":"Back-End Development","title":"Back-End Development"},{"payload":"Front-End Development","title":"Front-End Development"},{"payload":"Fullstack","title":"Fullstack"}]
        design_sub_role_list=[{"payload":"UX" ,"title": "UX only"},{"payload":"UI","title": "UI only"},{"payload":"UI/UX","title":"mix of both"}]
        network_sub_role_list=[{"payload":"Security" ,"title": "Security Specialist"},{"payload":"Network Specialist","title": "Network Specialist"},{"payload":"Security Network","title":"Security Network"}]
        Marketing_sub_role_list=[{"payload":"Digital Marketing" ,"title": "Digital Marketing"},{"payload":"Product Marketing","title": "Product Marketing"}]
        btnmsg=""
        btnlist =[]
        if(role=="Software Development"):       
            btnlist=dev_sub_role_list
            btnmsg="Why don't you pick your prefered development role 👇"
        elif (role=="UI/UX Design"):
            btnlist=design_sub_role_list
            btnmsg="That's great. We may have an opening in UI/UX Design 😃"
        elif(role =="Security and network"):
            btnmsg="what is your speciality ?😃"
            btnlist=network_sub_role_list
        elif(role =="Marketing"):
            btnmsg="which one are you you more interested in?😃"
            btnlist=Marketing_sub_role_list

        if(btnlist):
            buttons = []
            for btn in btnlist:
                title = (btn["title"])
                payload = ( btn["payload"])
                buttons.append({ "title": title, "payload": payload })
            dispatcher.utter_button_message(btnmsg, buttons)
        else:
            dispatcher.utter_template("action_job",Tracker)
        return   []      

class jobs_form(FormAction):
    """Example of a custom form action"""
    def name(self):
        """Unique identifier of the form"""
        return "jobs_form"
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["jobRef"]
    def submit(self, dispatcher, tracker, domain):
        jobRef = tracker.get_slot("jobRef")
        dispatcher.utter_template('utter_ask_apply', tracker)
        return []

#internship actions
class InternshipAction(Action):
    def name(self):
        return "action_internship"
    def run(self, dispatcher, tracker, domain):
        user_id = (tracker.current_state())["sender_id"] 
        #user_id = "189c6a81-abde-4388-a757-a50da959e8da"

        # get all internship reference and project title ( recommended )
        possible_internships = list_internships(user_id)

        message = "These are the available internship offers that we have right now, use the Internship Reference to learn more about an offer!"

        # generates a list of buttons from the list of possible_internships
        buttons = generate_internship_buttons(possible_internships)

        dispatcher.utter_button_message(message, buttons)
        return []
        
class internshipform(FormAction):
    """Example of a custom form action"""
    def name(self):
        """Unique identifier of the form"""
        return "internship_form"
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["internshipRef"]
    def submit(self, dispatcher, tracker, domain):
        job_title = tracker.get_slot("internshipRef")
        dispatcher.utter_template('utter_submit', tracker)
        return []

class Actioncontact(Action):
    def name(self):
        return "action_contact"
    def run(self, dispatcher, tracker, domain):
        user_id = (tracker.current_state())["sender_id"]        
        #get contact of user_id 
        dispatcher.utter_message("hello")
        return []

# Job Option Action
class actionShowDetails(Action):
    def name(self):
        return "action_show_details"
    def run(self, dispatcher, tracker, domain):
        jobRef = tracker.get_slot("jobRef")
        job_option = tracker.get_slot("JobOptions")
        #user_id = (tracker.current_state())["sender_id"]
        user_id = "189c6a81-abde-4388-a757-a50da959e8da"
        #getting data from DB
        job_data = get_job_data(job_option, jobRef, user_id)

        #put stuff from DB here 
        dispatcher.utter_message(f"{job_data}")
        return []

class actionAcquaintance(Action):
    def name(self):
        return "action_acquaintance"
    def run(self, dispatcher, tracker, domain):
        user_id = (tracker.current_state())["sender_id"]
        #data from data base here 
        dispatcher.utter_message("get acquaintance" + user_id)
        return []

class ApplyForm(FormAction):
    """Example of a custom form action"""
    def name(self):
        # type: () -> Text
        """Unique identifier of the form"""
        return "apply_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["jobRef","name", "experience_years",
                "phone_number", "email","cv_link"]

    def slot_mappings(self):
        # type: () -> Dict[Text: Union[Dict, List[Dict]]]
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {"jobRef": self.from_entity(entity="jobRef",
                                            intent=["inform_apply"]),
                "name": self.from_entity(entity="name",
                                                intent="inform_apply"),                            
                "experience_years": [self.from_entity(entity="experience_years",
                                                intent=["inform_apply",
                                                        "apply_job"]),
                               self.from_entity(entity="experience_years")],
                "phone_number": [self.from_entity(entity="phone_number", intent=["inform","apply_job"]),
                               self.from_entity(entity="phone_number")],
                "email": [self.from_entity(entity="email", intent=["inform","apply_job"]),
                               self.from_entity(entity="email")],
                "cv_link": [self.from_entity(entity="cv_link", intent=["inform","apply_job"]),
                               self.from_entity(entity="cv_link")]}

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer"""
        try:
            int(string)
            return True
        except ValueError:
            return False

    def validate_experience_years(self,
                            value: Text,
                            dispatcher: CollectingDispatcher,
                            tracker: Tracker,
                            domain: Dict[Text, Any]) -> Optional[Text]:
        """Validate experience years value."""

        if self.is_int(value) and int(value) > 0:
            return value
        else:
            dispatcher.utter_template('utter_wrong_experience_years', tracker)
            # validation failed, set slot to None
            return None
    @staticmethod
    def validate_email(value: Text,
                                 dispatcher: CollectingDispatcher,
                                 tracker: Tracker,
                                 domain: Dict[Text, Any]) -> Any:

        EMAIL_REGEX = re.compile(r"[a-z A-Z]+[0-9 a-z A-Z]*@[a-z A-Z]+[.][a-z A-Z]+")
        if EMAIL_REGEX.match(value):
            return value
        else:
            dispatcher.utter_template('utter_wrong_email', tracker)
            # validation failed, set slot to None
            return None
    @staticmethod
    def validate_cv_link(value: Text,
                                 dispatcher: CollectingDispatcher,
                                 tracker: Tracker,
                                 domain: Dict[Text, Any]) -> Any:
        CV_LINK_REGEX = re.compile(r"[https:\\/\\/]*[www.]*[a-z]*.*[com|org|tn|fr|me]+*[\\/in\\/]*[a-z A-z 0-9 -]+")
        if CV_LINK_REGEX.match(value):
            return value
        else:
            dispatcher.utter_template('utter_wrong_cv_link', tracker)
            # validation failed, set slot to None
            return None

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        """in other words from here the applicant data goes to the database"""    
        # utter submit template
        dispatcher.utter_template('action_store_applicant', tracker)
        return []
#this doesn't work i dunno why
class actionstoreApplicant(Action):
    def name(self):
        return "action_store_applicant"
    def run(self, dispatcher, tracker, domain):
        jobRef=tracker.get_slot("jobRef")
        name =tracker.get_slot("name")
        experience_years=tracker.get_slot("experience_years")
        phone_number=tracker.get_slot("phone_number")
        email = tracker.get_slot("email")
        cv_link=tracker.get_slot("cv_link")
        user_id = (tracker.current_state())["sender_id"]
        saveApplicantData(jobRef,name,experience_years,phone_number,email,cv_link, user_id)
        dispatcher.utter_message("we got your data, we will contact you soon")
        return[]
        