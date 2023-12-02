from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DailyEventForm, ScheduleForm
from .models import Schedule, ScheduleCalendar


#view for logging in
def loginView(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    return render(request, "testing/login.html")


def testHome(request):
    
    return render(request, 'testing/sched-cals.html')


def addDailyevent(request):
    form = DailyEventForm()

    if request.method == "POST":
        form = DailyEventForm(request.POST)
        if form.is_valid():
            
            pass

    return render(request, "testing/form.html", {"form": form})


def addSchedule(request):
    calendars = ScheduleCalendar.objects.filter(owner=request.user)

    form = ScheduleForm(request.user)
    
    if request.method == "POST":
        form = ScheduleForm(request.user,request.POST)
       
        if form.is_valid():
            print(type(form.cleaned_data["calendar"]))
            print(form.cleaned_data["name"])

            schedule = form.save()
            return redirect('add-schedule')

    return render(request, "testing/form.html", {"form": form})
