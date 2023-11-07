from django.shortcuts import render
from django.http import HttpResponse
from .forms import DailyEventForm, ScheduleForm
from .models import Schedule, ScheduleCalendar


# Create your views here.
def testHome(request):
    return HttpResponse("Hello")


def addDailyevent(request):
    form = DailyEventForm()

    if request.method == "POST":
        form = DailyEventForm(request.POST)
        if form.is_valid():
            # print(form.fields)
            pass

    return render(request, "testing/form.html", {"form": form})


def addSchedule(request):
    calendars = ScheduleCalendar.objects.filter(owner=request.user)

    form = ScheduleForm(request.user)
    print(form)
    if request.method == "POST":
        form = ScheduleForm(request.user,request.POST)
        print(form)
        if form.is_valid():
            print(type(form.cleaned_data["calendar"]))
            print(form.cleaned_data["name"])
    return render(request, "testing/form.html", {"form": form})
