from django.core.checks import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate

import datetime
from .models import System_database, Student_database
from Specialtopic.admin import System_databaseResource

# Create your views here.

# Necessary global variables.
user = None
systems = [("s1", "System 1"), ("s2", "System 2"), ("s3", "System 3")]
kindles = [("k1", "Kindle 1"), ("k2", "Kindle 2")]
assigned_system = []
assigned_list = []


def index(request):
    return render(request, "entry_system/index.html")


def details(request):
    return render(request, "entry_system/details.html")    


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        token = request.POST.get("password")
        # print(username, token)
        user = authenticate(username = username, password = token)
        # print(user)
        if user is not None:
            return redirect("http://127.0.0.1:8000/index.html/")
        else:
            return redirect("http://127.0.0.1:8000/")

    return render(request, "login/login.html")


def pending(request):
    student_usn = request.POST.get("allocated_system")
    time_out = request.POST.get("time_out")
    timed_out_system = []
    
    if time_out is not None:
        for i, details in enumerate(assigned_list):
            if (student_usn in details):
                
                details.append(time_out)
                # print("1",timed_out_system)
                # print("2",assigned_list)
                System_database.objects.create(Date = datetime.date.today(), Student_name = details[1], Branch = details[2], USN = details[0], System_no = details[3], Time_in = details[4], Time_out = details[5])
                del assigned_list[i]
        print(assigned_list[1:])
    return render(request, "entry_system/pending.html", {"assigned" : assigned_list[1:]})


def report(request):
    report_list = []
    today = datetime.date.today()
    query = System_database.objects.filter(Date__year = datetime.datetime.now().year, Date__month = datetime.datetime.now().month, Date__day = datetime.datetime.now().day)
    dataset = System_databaseResource().export(query)
    query_result = str(dataset.csv).split('\r\n')
    del query_result[0]
    del query_result[-1]
    for i in query_result:
        report_list.append(i.split(","))
    # print(report_list)
    return render(request, "entry_system/report.html", {"report" : report_list})
  
  
def contact(request):
    return render(request, "entry_system/contact.html")
  
  
def scan(request):
    student_name = request.POST.get("student_name")
    student_usn = request.POST.get("student_usn")
    student_department = request.POST.get("Department")
    system_no = request.POST.get("allocated_system")
    
    print(student_usn)
    
    if(system_no == "none"):
        system_no = request.POST.get("allocated_kindle")
    
    time_in = request.POST.get("time_in")
    assigned_list.append([student_usn, student_name, student_department, system_no, time_in])
    
    for i, system in enumerate(systems):
        if(system_no in system):
            assigned_system.append(system)
            del systems[i-1]

    for i, kindle in enumerate(kindles):
        if(system_no in kindle):
            assigned_system.append(kindle)
            del kindles[i-1]

    # print(student_name, student_usn, student_department, system_no, time_in)
    return render(request, "entry_system/scan.html", {"system" : systems, "kindle" : kindles})
