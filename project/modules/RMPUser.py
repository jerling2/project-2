from project.modules.RateMyProfessorAPI.ratemyprofessor.main import get_school_by_name, get_professor_by_school_and_name

"""
Using Rate My professor API to get University of Oregon professor data for website.
Rate My Professor API used: https://github.com/Nobelz/RateMyProfessorAPI/blob/master/ratemyprofessor/professor.py
"""

def create_dict_profs(prof_names: list):

    school = get_school_by_name("University of Oregon")

    if school is None:
        print("School Failure!")
        exit(0)

    professors = []
    for prof in prof_names:
        professors.append(get_professor_by_school_and_name(school, prof))

    prof_dic = {}

    for prof in professors:
        if (prof is None):
            continue
        prof_dic[f"{prof.name}"] = {
            "self" : prof,
            "difficulty" : prof.difficulty,
            "rating" : prof.rating,
            "numRatings" : prof.num_ratings,
            "department" : prof.department,
            "wouldTakeAgainPercent" : prof.would_take_again,
            "school" : prof.school,
            "courses" : prof.courses,
            "ratings" : prof.get_ratings()
        }

    return prof_dic

    


""" 
Each professor can access each individual rating as follows:

for i in prof.get_ratings():
    print("Class: "+i.class_name)
    print("--------------------------------") 
    print("Rating: " + str(i.rating)+"/5")
    print("Difficulty: " + str(i.difficulty)+"/5") 
    print("Take Again: " + str(i.take_again))
    print("Grade: " + str(i.grade))
    print("Number of Thumbs Up: " + str(i.thumbs_up))
    print("Number of Thumbs Down: " + str(i.thumbs_down))
    print("Online Class: " + str(i.online_class))
    print("For Credit: " + str(i.credit))
    print("Attendance: " + str(i.attendance_mandatory))
    print("Comment: " + i.comment)
    print("--------------------------------")

 """
"""
{"Geoff Brendel" : {
    "difficulty" : 3,
    "rating" : 3,
    "reviews" : {
        "review1" : {
            "course" : CS422,
            "rating" : 3,
            "difficulty" : 4,
            ect ...    
        }
        "review2" : {
            "course" CS330
            ect ...
        }
        .
        .
        .
        "reviewN"{
            data ...
        }
    }
    "num_reviews" : 7,
    ect ...
}


}
"""