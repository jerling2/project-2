# ------------------------------ Module Imports ------------------------------ #
from ..RateMyProfessorAPI.ratemyprofessor.main import get_school_by_name, get_professor_by_school_and_name
from ..GrandExchange.grand_exchange import Component
import logging

# ------------------------------- Logger Config ------------------------------ #
logger = logging.getLogger("project")
logger.setLevel(logging.INFO)


# --------------------------- Listening on Channels -------------------------- #
RMP_API_IN_CHANNELS = ["interval cycle"] 


# --------------------------- Publishing to Channels ------------------------- #
RMP_API_OUT_CHANNELS = ["rmp data"]


# --------------------------- RMP API Communicator --------------------------- #
class RMPAPICommunicator(Component):
    def __init__(self):
        super().__init__()
        self.subscribe_to_channels()
        self.prof_names = []
        self.school = None
        logger.info("RMP API Communicator initalized!")

    def subscribe_to_channels(self):
        """ This is called upon initialization """
        for channel in RMP_API_IN_CHANNELS:
            self.subscribe(channel)

    def set_prof_names(self, prof_names):
        self.prof_names = prof_names

    def set_school(self, school_name):
        school = get_school_by_name(school_name)
        if school is None:
            logger.warning(school_dne_warning(school))
            return None
        self.school= school

    def _get_prof_objects(self):
        if len(self.prof_names) == 0:
            logger.warning(prof_names_is_empty())
            return None
        
        if self.school is None:
            logger.warning(school_is_empty())
            return None

        prof_objects_list = []
        for name in self.prof_names:
            prof = get_professor_by_school_and_name(self.school, name)
            if prof is not None:
                prof_objects_list.append(prof)

        if len(prof_objects_list) == 0:
            logger.warning(prof_objects_list_is_empty())
            return None
        
        return prof_objects_list

    def create_prof_dict(self):
        profs = self._get_prof_objects()

        if profs is None:
            # Something went wrong.
            return None

        prof_dict = dict()
        for prof in profs:
            prof_dict[prof.name] = {}
            prof_dict[prof.name]["difficulty"] = prof.difficulty
            prof_dict[prof.name]["rating"] = prof.rating
            prof_dict[prof.name]["numRatings"] = prof.num_ratings
            prof_dict[prof.name]["department"] = prof.department
            prof_dict[prof.name]["school"] = prof.school.name
            if prof.would_take_again == None:
                prof_dict[prof.name]["wouldTakeAgainPercent"] = 0
            else:
                prof_dict[prof.name]["wouldTakeAgainPercent"] = prof.would_take_again
            prof_dict[prof.name]["courses"] = []
            for course in prof.courses:
                prof_dict[prof.name]["courses"].append(course.name)
        return prof_dict

    def notify(self, topic: str, message: object):
        """ This is called on when this component recieves a message """
        logging.info("Extracting Information from Rate My Professor ... ")
        prof_dict = self.create_prof_dict()
        logging.info("Done")
        for channel in RMP_API_OUT_CHANNELS:
            self.publish(channel, prof_dict)


# ----------------- Create Instance of  RMP API Communicator ----------------- #
# This will get executed when this file is imported. If this file is imported
# for a second time, this will not be executed again.
rmp_api_communicator = RMPAPICommunicator()
rmp_api_communicator.set_prof_names(["Hank Childs", "Zena Ariola", "Jee Choi", "Phil Colbert", "Dejing Dou", "Brittany Erickson"])
rmp_api_communicator.set_school("University of Oregon")
rmp_api_communicator.notify('', '')


# --------------------------------- Warnings --------------------------------- #
def school_dne_warning(school):
    warnMsg = "!!!!!!!\n"
    warnMsg +=  f"WARNING: RMPAPICommunicator : set_school() : "
    warnMsg += f"School: `{school}` does not exist.\n"
    warnMsg += "!!!!!!!"
    return warnMsg

def prof_names_is_empty():
    warnMsg = "!!!!!!!\n"
    warnMsg +=  f"WARNING: RMPAPICommunicator : get_prof_objects() : "
    warnMsg += f"self.profs_names (list) is empty.\n"
    warnMsg += "!!!!!!!"
    return warnMsg

def school_is_empty():
    warnMsg = "!!!!!!!\n"
    warnMsg +=  f"WARNING: RMPAPICommunicator : get_prof_objects() : "
    warnMsg += f"self.school (str) is None.\n"
    warnMsg += "!!!!!!!"
    return warnMsg

def prof_objects_list_is_empty():
    warnMsg = "!!!!!!!\n"
    warnMsg +=  f"WARNING: RMPAPICommunicator : get_prof_objects() : "
    warnMsg += f"prof_object_list was empty.\n"
    warnMsg += "!!!!!!!"
    return warnMsg