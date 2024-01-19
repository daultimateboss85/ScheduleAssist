from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DailyEventForm, ScheduleForm
from .models import Schedule, ScheduleCalendar


#view for logging in
def loginView(request):
    if request.user.is_authenticated:
        #problem is since not session authentication loginView will always be called
        #guess ill add some js in template to redirect to home page
        #so in template we link js file
        #if token is set in js file we redirect
        #else we display form
        return redirect("home")
    
    return render(request, "testing/login.html")


def Home(request):
    return render(request, 'testing/sched-cals.html')

