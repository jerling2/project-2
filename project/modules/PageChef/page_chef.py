# from ..GrandExchange.grand_exchange import Component
from ..GrandExchange.grand_exchange import Component
from enum import Enum
import logging
import os

# ------------------------------- Logger Config ------------------------------ #
logger = logging.getLogger("project")


# --------------------------- Listening on Channels -------------------------- #
PAGE_CHEF_IN_CHANNELS = ["rmp data"]


# --------------------------- Publishing to Channels ------------------------- #
PAGE_CHEF_OUT_CHANNELS = []


# ------------------------------- Recipe Book ------------------------------- #
class RecipeBook(Enum):
    PROF_PAGE_START = '/professors_page_start_recipe.txt'
    PROF_CONTAINER  = '/prof_container_recipe.txt'
    PROF_PAGE_END = '/professors_page_end_recipe.txt'


# -------------------------------- Page Chef -------------------------------- #
class PageChef(Component):
    def __init__(self):
        super().__init__()
        self.subscribeToAll()
        logger.info("Page Chef initalized!")

    
    def subscribeToAll(self):
        for channel in PAGE_CHEF_IN_CHANNELS:
            self.subscribe(channel)

    def cook(self, recipe, groceries=None):
        logger.info(f"PageChef: Cooking the '{recipe}' recipe.")
    
        module_path = os.path.dirname(__file__)
        recipe = open(module_path + "/" + recipe, "r")
        dish = ""
        for line in recipe:
            if line.startswith("!variable"):
                requested_ingredient = line.split()[1]
                ingredient = groceries.get(requested_ingredient)
                if ingredient is None:
                    missing_ingredient_warning(requested_ingredient)
                    dish += 'None\n'
                else:
                    dish += str(ingredient) + "\n"
            else:
                dish += line
        recipe.close()
        return dish

    def write_file(self, filename, page):
        module_path = os.path.dirname(__file__)
        relative_path = module_path + filename
        file = open(relative_path, 'w')
        file.write(page)
        file.close()
        return None

    def update_prof_page(self, rmp_data):
        page = ""
        page += self.cook(RecipeBook.PROF_PAGE_START.value)
        for key, value in rmp_data.items():
            prof_data = {}
            prof_data["prof_name"] = key
            prof_data["quality_score"] = value.get('rating')
            prof_data["difficulty_score"] = value.get('difficulty')
            would_take_again_score = value.get('wouldTakeAgainPercent')
            if would_take_again_score == -1:
                would_take_again_score = 'N/A'
            else:
                would_take_again_score = str(would_take_again_score) + '%'
            prof_data["would_take_again_score"] = would_take_again_score
            prof_data["number_ratings"] = str(value.get('numRatings')) + " reviews"
            page += self.cook(RecipeBook.PROF_CONTAINER.value, groceries=prof_data)
        page += self.cook(RecipeBook.PROF_PAGE_END.value)
        self.write_file('/../../templates/professors.html', page)
        return None

    def notify(self, topic: str, message: object):
        """ Do something when notified. """
        if topic == "rmp data":
            page = self.update_prof_page(rmp_data=message)


# ----------------- Create Instance of  RMP API Communicator ----------------- #
# This will get executed when this file is imported. If this file is imported
# for a second time, this will not be executed again.
page_chef = PageChef()


# --------------------------------- Warnings --------------------------------- #
def missing_ingredient_warning(ingredient):
    warn_msg = "!!!!!!!\n"
    warn_msg += f"Missing the '{ingredient}' ingredient! "
    warn_msg += "The dish will not be as tasty."
    warn_msg += "\n!!!!!!!"
    logger.warning(warn_msg)
