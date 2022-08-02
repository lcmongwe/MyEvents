
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Venue(models.Model):
    name = models.CharField('Venue Name',max_length=120)
    address=models.CharField('Address',max_length=300)
    zip_code=models.CharField('Zip Code',max_length=15)
    phone = models.CharField('Contact Phone',max_length=25,blank=True)
    web=models.URLField('Website Address',blank=True)
    email_address=models.EmailField('Email',blank=True)
    owner=models.IntegerField('venue owner',blank=False, default=1)

    def __str__(self):
        return self.name

class MyClubUser(models.Model):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    email= models.EmailField('User Email ')
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    name = models.CharField('Event Name',max_length=120)
    event_date = models.DateTimeField('Event date')
    venue = models.ForeignKey(Venue,blank=True,null=True,on_delete=models.CASCADE)
    # venue=models.CharField(max_length=120)
    manager=models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL)
    description = models.TextField('Description', blank=True)
    attendees = models.ManyToManyField(MyClubUser,blank=True)

    def __str__(self):
        return self.name