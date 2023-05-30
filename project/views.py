from django.shortcuts import render
def index(request):
    return render(request, "index.html")

def schedulebuilder(request):
    return render(request, "schedulebuilder.html")

def professors(request):
    return render(request, "professors.html")

def courses(request):
    return render(request, "courses.html")

def degreereqs(request):
    return render(request, "degreereqs.html")