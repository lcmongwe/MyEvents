from django.shortcuts import render,redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event,Venue
from django.contrib.auth.models import User
from .forms import VenueForm,EventForm,EventFormAdmin
from django.http import HttpResponse
import csv
from django.contrib import messages

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# import paginator
from django.core.paginator import Paginator


def my_events(request):
    if request.user.is_authenticated:
        me=request.user.id
        events=Event.objects.filter(attendees=me)
        return render(request,'events/my_events.html' ,{'me':me,'events':events})
    else:
        messages.success(request,('you are not authorised to view this page'))
        return redirect('home')

# generate a pdf venue file
def venue_pdf(request):
    buf=io.BytesIO()
    # create a canvas
    c=canvas.Canvas(buf,pagesize=letter,bottomup=0)

    # create a text object
    textob=c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont('Helvetica',14)

    # add some test lines of text
    # lines=[
    # 'this is line1',
    # 'this is line2',
    # 'this is line3',]
    venues=Venue.objects.all()
    lines=[]

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append('======================== ')
    # loop
    for line in lines:
        textob.textLines(line)
    # finish up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf,as_attachment=True,filename='venue.pdf')


# generate csvfile venus list
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
 
#  create a csv writer
    writer=csv.writer(response)
    # designate the model
    venues =Venue.objects.all()

    # add column headings to csv file
    writer.writerow(['Venue Name','Address','zip code','phone','web address','email address',])
    # create blank list
    
    # loop through and output
    for venue in venues:
        writer.writerow([venue.name,venue.address,venue.zip_code,venue.phone,venue.web,venue.email_address])

    return response

# generate textfile venus list
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    # lines=['this is line1', 'this is line2', 'this is line3']
    venues =Venue.objects.all()
    # create blank list
    lines = []
    # loop through and output
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n\n')

    # write text file
    response.writelines(lines)
    return response

# Create your views here.
def delete_venue(request, venue_id):
    venue=Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list_venues')

def delete_event(request, event_id):
    event=Event.objects.get(pk=event_id)
    if request.user==event.manager:
        event.delete()
        messages.success(request,('event deleted'))
        return redirect('list_events')

    else:
        messages.success(request,('you are not allowed to delete this event'))
        
    return redirect('list_events')


def add_event(request):
    submitted=False
    if request.method == "POST":
        if request.user.is_superuser:
            form=EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form=EventForm(request.POST)
            if form.is_valid():
                event=form.save(commit=False)
                event.manager=request.user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        # just going to the form not submitting
        if request.user.is_superuser:
            form=EventFormAdmin()
        else:
            form=EventForm
        if 'submitted' in request.GET:
            submitted=True

    return render(request, 'events/add_event.html',{'form':form,'submitted':submitted})


def update_venue(request,venue_id):
    venue=Venue.objects.get(pk=venue_id)
    form=VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list_venues')
    return render(request, 'events/update_venue.html',{'venue':venue,'form':form})

def update_event(request,event_id):
    event=Event.objects.get(pk=event_id)
    if request.user.is_superuser:

        form=EventFormAdmin(request.POST or None, instance= event)
    else:
        form=EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list_events')
    return render(request, 'events/update_event.html',{'event':event,'form':form})


def search_venues(request):
    if request.method == 'POST':
        searched=request.POST.get('searched')
        venues=Venue.objects.filter(name__contains=searched)
        return render(request, 'events/search_veneus.html',{'searched':searched,'venues':venues})
       

    else:
        return render(request, 'events/search_veneus.html',{})


def show_venue(request,venue_id):
    venue=Venue.objects.get(pk=venue_id)
    venue_owner=User.objects.get(pk=venue.owner)
    return render(request, 'events/show_venue.html',{'venue':venue,'venue_owner':venue_owner})

def list_venues(request):
    venue_list=Venue.objects.all()

    # set up pagination
    p = Paginator(Venue.objects.all(), 2)
    page = request.GET.get('page')
    venues = p.get_page(page)

    return render(request, 'events/venues.html',{'venue_list':venue_list ,'venues':venues})


def add_venue(request):
    submitted=False
    if request.method == "POST":
        form=VenueForm(request.POST)
        if form.is_valid():
            venue=form.save(commit=False)
            venue.owner=request.user.id
            venue.save()
            # form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form=VenueForm
        if 'submitted' in request.GET:
            submitted=True

    return render(request, 'events/add-venue.html',{'form':form,'submitted':submitted})


def all_events(request):
    event_list=Event.objects.all().order_by('-name')
    return render(request, 'events/events_list.html',{'event_list':event_list})


def home(request,year= datetime.now().year,month=datetime.now().strftime('%B')):
    name ='lucy'
    month=month.capitalize()

    # convert month from string to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create a calender
    cal= HTMLCalendar().formatmonth(year,month_number)

    # get current year
    now=datetime.now()
    current_year=now.year
    time=now.strftime('%I:%M:%S %p')

    return render(request, 'events/home.html',{'name':name,
    'year':year,'month':month, 'month_number':month_number,'cal':cal,'current_year':current_year,'time':time})