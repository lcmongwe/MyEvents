from django import forms
from django.forms import ModelForm
from .models import Venue,Event

# create admin superuser event form
class EventFormAdmin(ModelForm):
    class Meta:
        model= Event
        # fields= "__all"
        fields=('name', 'event_date', 'venue','manager', 'attendees', 'description',  )

        labels={
            'name':'',
            'event_date':'YYYY-MM-DD HH:MM:SS',
            'venue':'venue',
            'manager':'manager',
            'attendees':'attendees',
            'description':'',
           
        }

        widgets={
           'name': forms.TextInput(attrs={'class': 'form-control','placeholder':' event name '}),
           'event_date':forms.TextInput(attrs={'class': 'form-control','placeholder':'event date'}),
           'venue':forms.Select(attrs={'class': 'form-control','placeholder':'venue'}),
           'manager':forms.Select(attrs={'class': 'form-control','placeholder':'manager'}),
           'attendees':forms.SelectMultiple(attrs={'class': 'form-control','placeholder':'attendees'}),
           'description':forms.Textarea(attrs={'class': 'form-control','placeholder':'description'}),
           
        }




# create user event from
class EventForm(ModelForm):
    class Meta:
        model= Event
        # fields= "__all"
        fields=('name', 'event_date', 'venue', 'attendees', 'description',  )

        labels={
            'name':'',
            'event_date':'YYYY-MM-DD HH:MM:SS',
            'venue':'venue',
            
            'attendees':'attendees',
            'description':'',
           
        }

        widgets={
           'name': forms.TextInput(attrs={'class': 'form-control','placeholder':' event name '}),
           'event_date':forms.TextInput(attrs={'class': 'form-control','placeholder':'event date'}),
           'venue':forms.Select(attrs={'class': 'form-control','placeholder':'venue'}),
           
           'attendees':forms.SelectMultiple(attrs={'class': 'form-control','placeholder':'attendees'}),
           'description':forms.Textarea(attrs={'class': 'form-control','placeholder':'description'}),
           
        }



# create a venue form
class VenueForm(ModelForm):
    class Meta:
        model= Venue
        # fields= "__all"
        fields=('name', 'address', 'zip_code',  'phone', 'web','email_address', )

        labels={
            'name':'',
            'address':'',
            'zip_code':'',
            'phone':'',
            'web':'',
            'email_address':'',
        }

        widgets={
           'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'venue '}),
           'address':forms.TextInput(attrs={'class': 'form-control','placeholder':' address'}),
           'zip_code':forms.TextInput(attrs={'class': 'form-control','placeholder':'zip code'}),
           'phone':forms.TextInput(attrs={'class': 'form-control','placeholder':'contact phone'}),
           'web':forms.EmailInput(attrs={'class': 'form-control','placeholder':'web address'}),
           'email_address':forms.TextInput(attrs={'class': 'form-control','placeholder':'email_address'})
        }