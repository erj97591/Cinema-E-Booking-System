from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from encrypted_model_fields.fields import EncryptedIntegerField, EncryptedDateField
from django.utils import timezone
from datetime import datetime, timedelta, time, date
from django.core.exceptions import ValidationError
from  embed_video.fields  import  EmbedVideoField 
from django.utils.translation import gettext_lazy as _ 
from django_extensions.db.fields import AutoSlugField



class ShowRoom(models.Model):
    room_number = models.IntegerField()
    number_seats = models.IntegerField()

    def __str__(self):
        return str(self.room_number)
'''
class ShowTime(models.Model):
    show_id = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    duration = models.DurationField()
    #movie = models.ForeignKey(Movie, on_delete=models.CASCADE, default=None)
    #show_room = models.ForeignKey(ShowRoom, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return str(self.show_id)
'''
class Movie(models.Model):
    title = models.CharField(max_length=100)
    cast = models.CharField(max_length=500)
    #trailer = models.URLField(default="https://www.youtube.com/watch?v=iw_wt2hHW2w")
    trailer = EmbedVideoField()
    synopsis = models.CharField(max_length=500)
    category = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)
    picture = models.ImageField(blank=True, upload_to='movies')
    rating =  models.CharField(max_length=100)
    #slug = models.SlugField(null=True)
    slug = AutoSlugField(null=True, populate_from='title')
    duration = models.DurationField(default=timedelta(hours=2, minutes=30))

    def isShowing(self):
        query = ShowTime.objects.filter(movie__title=self.title)
        if query :
        #if Movie.showtime.exists():
            #Showtime.objects.filter(movie__title=self.title)
            return True
        else:
            return False

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})

class ShowTime(models.Model):
    date = models.DateField(default=date.today())
    time = models.TimeField(default=time(9,30,0))
    movie = models.ForeignKey(Movie, related_name='showtimes', on_delete=models.CASCADE)
    show_room = models.ForeignKey(ShowRoom, on_delete=models.CASCADE)
    #slug = models.SlugField(null=True)
    slug = AutoSlugField(null=True, populate_from=['movie', 'date', 'time'])
    def __str__(self):
        return str(f'|{self.movie} {datetime.combine(self.date, self.time)}|')
    def clean(self):
        try:
            self.movie
        except:
            raise ValidationError("Movie Cannot Be Null")
        try:
            self.show_room
        except:
            raise ValidationError("Show room Cannot Be Null")
        show_times = ShowTime.objects.filter(show_room=self.show_room).filter(date=self.date).exclude(id=self.id)
        if show_times is not None:
            start_a = datetime.combine(self.date, self.time)
            end_a = start_a + self.movie.duration
            for show_time in show_times:
                start_b = datetime.combine(show_time.date,show_time.time)
                end_b = start_b + show_time.movie.duration

                print(f'enda: {end_a}\n endb: {end_b}\n starta: {start_a}\n startb: {start_b}')
                if ((start_a <= end_b) and (end_a >= start_b)):
                    raise ValidationError("Movies Overlap")
                else:
                    print('mutually exclusive')

    def create_tickets(self):
        if not Ticket.objects.filter(showtime=self).exists():
            for seat in range(self.show_room.number_seats):
                Ticket(ticket_id=seat+1, showtime=self).save()

class Promotion(models.Model):
    promo_id = models.IntegerField()
    discount = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    send = models.BooleanField(default=False)

    def __str__(self):
        return str(self.promo_id)

class Booking(models.Model):

     booking_id = models.AutoField(primary_key=True)
     number_adult = models.IntegerField(null=True, blank=True, default="0")
     number_child = models.IntegerField(null=True, blank=True, default="0")
     number_senior = models.IntegerField(null=True, blank=True, default="0")
     booking_status = models.CharField(max_length=100, default = "inactive")
     showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE, null=True)
     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
     #tickets = MultiSelectField(choices = )

     def __str__(self):
        return str(self.booking_id)

     def number_tickets(self):
        return self.number_adult + self.number_child + self.number_senior

class Ticket(models.Model):
    ticket_id = models.IntegerField()
    booking = models.ForeignKey(Booking, related_name='tickets', on_delete=models.CASCADE, null=True)
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE, null=True)
    reserved = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.ticket_id)


class PaymentCard(models.Model):
    card_number = EncryptedIntegerField()
    expiration_date = EncryptedDateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.card_number)


class UpdateProfileModel(models.Model):
    phone_number = forms.IntegerField()
    address = forms.CharField(max_length=500, help_text='Address')
    promotions = models.BooleanField(default=False)

    def __str__(self):
        return str(self.phone_number)


class UpdateUserModel(models.Model):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    def __str__(self):
        return str(self.first_name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False)
    phone_number = models.IntegerField(null=True)
    address = models.CharField(max_length=500)
    promotions = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    #instance.profile.save()

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
