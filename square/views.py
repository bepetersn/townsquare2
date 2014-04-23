from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from square.models import Volunteer, Event
from square.forms import AddVolunteerForm, LoginForm, AddEventForm
from square.processing import process_volunteer, process_volunteer


def about(request):
    
    blurb = "Something about Townsquare."
    return render(request, 'users/about.html', 
                    {'blurb': blurb,})


def login(request):
    
    if request.method == 'POST':
        
        # POST request to login page does validation/processing
        form = LoginForm(request.POST)
        
        if form.is_valid():
            
            username = form.cleaned_data['Username']
            password = form.cleaned_data['Password']
        
            user = authenticate(username=username, password=password)
            
            
            if user is not None:
            
                if user.is_active:
                    
                    login(request, user)
                    return HttpResponseRedirect('/townsquare/volunteer/home')
                    
                else:

                    # this user is not allowed to access their account
                    return HttpResponseRedirect('/townsquare/login')
            
            else:
            
                return HttpResponseRedirect('/townsquare/login')
                
    
    return render(request, 'users/login.html', 
                    {'f': LoginForm()})


@login_required 
def home(request):
    
    #Assign the information on a single volunteer as an admin
    # NOTE: catch ObjectDoesNotExist exception here, as it may occur.
    va = Volunteer.objects.get(id=request.user.volunteer.id)
    
    return render(request, 'users/index.html',
                    {'va': va})


@login_required
def add_volunteer(request):
    if request.method == 'POST':
        
        # POST request to add_volunteer page does validation/processing
        form = AddVolunteerForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['Username']
            password = form.cleaned_data['Password']
            first = form.cleaned_data['first']
            last = form.cleaned_data['last']
            new_user = process_volunteer(first, last, username, password)

            return HttpResponseRedirect('/townsquare/volunteer/browse')

    else:
        # GET request to add_volunteer page displays an empty form
        form = AddVolunteerForm()

    return render(request, 'users/add_volunteer.html', 
                    {'f': form})


@login_required
def browse_volunteers(request):
    
    vols = Volunteer.objects.all()
    return render(request, 'users/volunteer_browse.html',
                    {'volunteers': vols,})
    
        
@login_required
def add_event(request):

    # POST request does processing
    if request.method == 'POST':

        form = AddEventForm(request.POST)

        if form.is_valid():

            evt = form.cleaned_data['event_type']
            evl = form.cleaned_data['event_location']
            d = form.cleaned_data['date']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            n = form.cleaned_data['notes']
            ivt = form.cleaned_data['is_volunteer_time']
            new_event = process_event(evt, evl, d, start, end, n, ivt)

            return HttpResponseRedirect('/townsquare/event/browse')

    else:
        # GET request sends an empty form
        form = AddEventForm()

    # render an HTTP response if it was a GET, or an invalid POST
    return render(request, 'users/add-event.html', 
                    {'f': form})


@login_required
def browse_events(request):
    
    evs = Event.objects.all()
    return render(request, 'users/event_browse.html',
                    {'events': evs,})
    
    
def logout(request):
    
    logout(request)
    return HttpResponse("Logged out")


