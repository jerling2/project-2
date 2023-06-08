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
import json
import math
# ------------------------------- Logger Config ------------------------------ #
logger = logging.getLogger("project")


# --------------------------- Listening on Channels -------------------------- #
PAGE_CHEF_IN_CHANNELS = ["rmp data", "db data"]


# --------------------------- Publishing to Channels ------------------------- #
PAGE_CHEF_OUT_CHANNELS = []


# ------------------------------- Recipe Book ------------------------------- #
#                   These are the Locations for Each Recipe                   #
class RecipeBook(Enum):
    PROF_PAGE_START = 'recipes/professors_static_start.txt'
    PROF_CONTAINER  = 'recipes/prof_dynamic_container.txt'
    PROF_PAGE_END = 'recipes/professors_static_end.txt'
    COURSE_PAGE_START = 'recipes/courses_static_start.txt'
    COURSE_CONTAINER_1 = 'recipes/courses_dynamic_container_1.txt'
    COURSE_CONTAINER_2 = 'recipes/courses_dynamic_container_2.txt'
    COURSE_CONTAINER_3 = 'recipes/courses_static_container_3.txt'
    COURSE_PAGE_END = 'recipes/courses_static_end.txt'
    SCHEDULE_PAGE_START = 'recipes/schedule_builder_static_start.txt'
    SCHEDULE_CONTAINER_1 = 'recipes/schedule_builder_dynamic_container_1.txt'
    SCHEDULE_PAGE_MIDDLE = 'recipes/schedule_builder_static_middle.txt'
    SCHEDULE_CONTAINER_2 = 'recipes/schedule_builder_dynamic_container_2.txt'
    SCHEDULE_PAGE_END = 'recipes/schedule_builder_static_end.txt'


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

        # Step 1: cook the static beginning part of the professor's page.
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
            page += self._cook(RecipeBook.PROF_CONTAINER.value, groceries=prof_data) + '\n'

        # Step 3: cook the static ending part of the professor's page.       
        page += self._cook(RecipeBook.PROF_PAGE_END.value)
        # Step 4: Write the file to the right path.
        self._write_file('/../../templates/professors.html', page)
        return None

    def update_courses_page(self, courses_data: dict):
        page = ""

        # Step 1: cook the static beginning part of the courses' page.
        page += self._cook(RecipeBook.COURSE_PAGE_START.value)

        # Sort the keys to make a more coherent order.
        sorted_keys = []
        for key in courses_data:
            sorted_keys.append(key)
        sorted_keys.sort()
        

        for key in sorted_keys:
            c_title = {'course_title': key}
            page += self._cook(RecipeBook.COURSE_CONTAINER_1.value, groceries=c_title) + '\n'
            
            data = courses_data[key]
            professor_length = len(courses_data[key]['professors'])
            for i in range(professor_length):
                prof_data = {}
                prof_data['professor'] = data['professors'][i]
                if data['schedule'][i] == 'TBA':
                    prof_data['time'] = "TBA"
                else:
                    prof_data['time'] = data['schedule'][i] + ' ' + data['time'][i] 
                page += self._cook(RecipeBook.COURSE_CONTAINER_2.value, groceries=prof_data) + '\n'

            page += self._cook(RecipeBook.COURSE_CONTAINER_3.value) + '\n'
        
        # Step 3: cook the static ending part of the courses' page.       
        page += self._cook(RecipeBook.COURSE_PAGE_END.value)

        # Step 4: Write the file to the right path.
        self._write_file('/../../templates/courses.html', page)
        return None

    def update_schedule_page(self, schedule_data: dict):
        page = ""

        day_dict = {'m': 1, 't': 2, 'w': 3, 'r': 4, 'f': 5}

        # Sort the keys to make a more coherent order.
        sorted_keys = []
        for key in schedule_data:
            sorted_keys.append(key)
        sorted_keys.sort()

        # Step 1: cook the static beginning part of the schedule's page.
        page += self._cook(RecipeBook.SCHEDULE_PAGE_START.value)
        
        for key in sorted_keys:
            data = schedule_data[key]
            professor_length = len(data['professors'])
                
            for i in range(professor_length):
                schedule = data['schedule'][i]
                # Skip this iteration if schedule does not contain m, t, w, r, or f.
                if not any(day in schedule for day in ['m', 't', 'w', 'r', 'f']):
                    continue

                course_name = key[:-3] + " " + key[-3:]
                css_class_name = key[:-3] + "-" + key[-3:]

                interval = data['time'][i].split('-')
                start = int(interval[0])
                end = int(interval[1])
                
                # this is an algorithim that transforms military time into a position
                # on the grid. I made it through trial and error, so I'm not exactly
                # sure on how it works.
                row_start = math.ceil((start-(math.floor((start-700)/100)*40)-699)/5)
                row_end = math.ceil((end-(math.floor((end-700)/100)*40)-699)/5)

                grid_row = f'grid-row: {row_start} / {row_end};'
                for day in schedule:
                    col = day_dict[day]
                    grid_col = f'grid-column: {col} / {col};'

                    container_1_data = {
                        'grid_row': grid_row, 
                        'grid_col': grid_col, 
                        'course_name': course_name,
                        'css_class_name': css_class_name
                    }
                  
                    page += self._cook(RecipeBook.SCHEDULE_CONTAINER_1.value,
                                       groceries=container_1_data) + '\n'


        # Step 3: cook the static middle part of the schedule's page.       
        page += self._cook(RecipeBook.SCHEDULE_PAGE_MIDDLE.value) + '\n'

        # Step 4: cook the dynamic container 2 part of the schedule's page. 
        for key in sorted_keys:
            data = schedule_data[key]
            schedule = data['schedule'][0]
            if not any(day in schedule for day in ['m', 't', 'w', 'r', 'f']):
                    continue
            course_name = key[:-3] + " " + key[-3:]
            container_2_data = {'course_name': course_name}
            page += self._cook(RecipeBook.SCHEDULE_CONTAINER_2.value,
                                groceries=container_2_data) + '\n'

        # Step 5: cook the static ending part of the schedule's page. 
        page += self._cook(RecipeBook.SCHEDULE_PAGE_END.value)

        # Step 4: Write the file to the right path.
        self._write_file('/../../templates/schedule_builder.html', page)
        return None


    def notify(self, topic: str, message: object):
        """ Do something when this component recieves a message. """
        if topic == "rmp data":
            if isinstance(message, dict) == False:
                malformed_groceries_warning(message)
                return None
            self.update_prof_page(rmp_data=message)
        elif topic == "db data":
            data = json.loads(message)
            self.update_courses_page(data)
            self.update_schedule_page(data)
                


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