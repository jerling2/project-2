from django.shortcuts import render
from project.modules.RMPUser import create_dict_profs
from django.http import JsonResponse
from django.core.cache import cache

import project.modules.PageChef.page_chef
<<<<<<< HEAD
import project.modules.RMPAPICommunicator.rmp_api_communicator
=======
# import project.modules.RMPAPICommunicator.rmp_api_communicator
>>>>>>> joseph
import project.modules.CourseDBCommunicator.courses_db_communicator



def index(request):
    return render(request, "index.html")

def schedulebuilder(request):
    return render(request, "schedule_builder.html")

def professors(request):
    return render(request, "professors.html")
    # # LOAD CONFIG FILE
        
    # prof_names = ["Hank Childs", "Zena Ariola", "Jee Choi", "Phil Colbert", "Dejing Dou", "Brittany Erickson"]
    # # Try to fetch the professor data from the cache
    # professor_data = cache.get('prof_data')
    
    # if professor_data is None:
    #     # If the data is not available in the cache, create it and store it in the cache
    #     professor_data = create_dict_profs(prof_names)
    #     cache.set('prof_data', professor_data)
    
    # return render(request, "professors.html", {"prof_names": prof_names})

def professor_data(request, professor):
    prof_data = cache.get('prof_data')
    
    if professor in prof_data:
        professor_data = prof_data[professor]
        return JsonResponse(professor_data)
    else:
        return JsonResponse({}, status=404)
    

def courses(request):
    return render(request, "courses.html")

def degreereqs(request):
    return render(request, "degreereqs.html")