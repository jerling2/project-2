"""
    Title: The Page Chef
    Brief: The Page Chef uses recipes and groceries to construct webpages. The
           recipes are text files that encode HTML that the page chef reads. 
           When the page chef comes across a line that starts with !variable,
           it adds the corresponding variable to the line. Groceries is an alias
           for data which is formated as a dictionary. 
    Author: Joseph.
"""
# ------------------------------ Module Imports ------------------------------ #
from ..GrandExchange.grand_exchange import Component
from enum import Enum
import logging
import os

# ------------------------------- Logger Config ------------------------------ #
logger = logging.getLogger("project")


# --------------------------- Listening on Channels -------------------------- #
PAGE_CHEF_IN_CHANNELS = ["rmp data", "db data"]


# --------------------------- Publishing to Channels ------------------------- #
PAGE_CHEF_OUT_CHANNELS = []


# ------------------------------- Recipe Book ------------------------------- #
#                   These are the Locations for Each Recipe                   #
class RecipeBook(Enum):
    PROF_PAGE_START = '/professors_page_start_recipe.txt'
    PROF_CONTAINER  = '/prof_container_recipe.txt'
    PROF_PAGE_END = '/professors_page_end_recipe.txt'


# -------------------------------- Page Chef -------------------------------- #
class PageChef(Component):
    """
        Brief: The PageChef creates HTML pages by filling in the template for
               the HTML page with values. The PageChef refers to the template
               as a 'recipe', the values that could be inserted into the recipe
               as 'grocieres', and the value that is inserted into the recipe
               as an 'ingredient'.
    """
    def __init__(self):
        super().__init__()
        self._subscribeToAll()
        logger.info("Page Chef initalized!")

    
    def _subscribeToAll(self):
        """ This is called upon initialization """
        for channel in PAGE_CHEF_IN_CHANNELS:
            self.subscribe(channel)

    def _cook(self, path_to_recipe: str, groceries: dict=None):
        """ The _cook method takes a path_to_a_recipe and groceries to 
            dynamically create an HTML page. The _cook method reads the recipe
            line by line, and checks to see if the line starts with '!variable`.
            If so, it splits the line and uses the second element of the line
            as a key to grab the ingredient from the groceries. If the
            ingredient is in the groceries, it adds the ingredient to the dish.
            Otherwise, it warns the user that they're missing an ingredient and
            adds 'None' to the dish. If the line didn't start with !variable,
            the _cook method adds the line to the dish. This allows for some
            recipes to be cooked without any grocieries.

            Parameters:
                1. path_to_recipe (str): 
                    the path to the recipe using the recipe book.
                2. grocieries (dict):
                    the dictionary data that is used to fill in the !variable. 

            Returns:
                dish (str): A string that encodes a valid HTML webpage.
        """
        logger.info(f"PageChef: Cooking the '{path_to_recipe}' recipe.")
        module_path = os.path.dirname(__file__)
        recipe = open(module_path + "/" + path_to_recipe, "r")
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

    def _write_file(self, relative_path_to_file: str, html_page_str: str):
        """ Write a file using a relative path and the HTML page string """
        absolute_path = os.path.dirname(__file__)
        path = absolute_path + relative_path_to_file
        file = open(path, 'w')
        file.write(html_page_str)
        file.close()
        return None

    def update_prof_page(self, rmp_data: dict):
        """ Create the professor's page by using three recipes """
        page = ""

        # Step 1: cook the beginning of the professor's page.
        page += self._cook(RecipeBook.PROF_PAGE_START.value)

        # Step 2: for each professor's data, make a professors container.
        for key, value in rmp_data.items():
            prof_data = {}
            prof_data["prof_name"] = key
            prof_data["quality_score"] = value.get('rating')
            prof_data["difficulty_score"] = value.get('difficulty')
            prof_data["number_ratings"] = str(value.get('numRatings')) + " reviews"
            # Ternary operation to format the W.T.A.S correctly.
            wtas = value.get('wouldTakeAgainPercent')
            prof_data["would_take_again_score"] =  'N/A' if wtas == -1 else str(wtas) + "%"
            # Now that we have the groceries and the recipe, its time to cook!
            page += self._cook(RecipeBook.PROF_CONTAINER.value, groceries=prof_data)

        # Step 3: cook the end of the professor's page.       
        page += self._cook(RecipeBook.PROF_PAGE_END.value)
        # Step 4: Write the file to the right path.
        self._write_file('/../../templates/professors.html', page)
        return None

    def notify(self, topic: str, message: object):
        """ Do something when this component recieves a message. """
        if topic == "rmp data":
            if isinstance(message, dict) == False:
                malformed_groceries_warning(message)
                return None
            page = self.update_prof_page(rmp_data=message)


# ----------------- Create Instance of  RMP API Communicator ----------------- #
# This will get executed when this file is imported. If this file is imported
# for a second time, this will not be executed again.
page_chef = PageChef()


# --------------------------------- Warnings --------------------------------- #
def malformed_groceries_warning(groceries):
    warn_msg = "!!!!!!!\n"
    warn_msg += "The groceries is not not a dictionary. " 
    warn_msg += "Failed to create the webpage.\n"
    warn_msg += f"data recieved = '{groceries}'"
    warn_msg += "\n!!!!!!!"
    logger.warning(warn_msg)

def missing_ingredient_warning(ingredient):
    warn_msg = "!!!!!!!\n"
    warn_msg += f"Missing the '{ingredient}' ingredient! "
    warn_msg += "The dish will not be as tasty."
    warn_msg += "\n!!!!!!!"
    logger.warning(warn_msg)