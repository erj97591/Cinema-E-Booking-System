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



class ShowRoom(models.Model):

    room_number = models.IntegerField()
    number_seats = models.IntegerField()

    def __str__(self):
        return str(self.room_number)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    cast = models.CharField(max_length=500)
    trailer = EmbedVideoField()
    synopsis = models.CharField(max_length=500)
    category = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)
    picture = models.ImageField(blank=True, upload_to='movies')
    rating = models.CharField(max_length=100)
    slug = models.SlugField(null=True)
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
                    self.create_tickets()

    def create_tickets(self):
        for seat in range(self.show_room.number_seats):
            Ticket(ticket_id=seat, showtime=self).save()



class Promotion(models.Model):
    promo_id = models.IntegerField()
    discount = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    send = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.promo_id)

class Booking(models.Model):
     #booking_id = models.IntegerField()
     booking_id = models.AutoField(primary_key=True)
     number_tickets = models.IntegerField()
     booking_status = models.CharField(max_length=100)
     #showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE)
     #user = models.ForeignKey(User, on_delete=models.CASCADE)

     def __str__(self):
        return str(self.booking_id)

class Ticket(models.Model):
    ticket_id = models.IntegerField()
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE)
    reserved = models.BooleanField(default=False)
    class TicketType(models.TextChoices):
        CHILD = 'C', _('Child')
        ADULT = 'A', _('Adult')
        SENIOR = 'S', _('Senior')

    ticket_type = models.CharField(
        max_length=1,
        choices=TicketType.choices,
        default=TicketType.ADULT,
    )
    def price(self):
        if self.ticket_type.CHILD:
            return "3"
        if self.ticket_type.ADULT:
            return "7"
        if self.ticket_type.SENIOR:
            return "5"



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
