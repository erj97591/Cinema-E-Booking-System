from unicodedata import category
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.db.models import Q
from .forms import RegistrationForm, PaymentForm, BookingForm, TicketForm
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Booking, PaymentCard, Movie, ShowTime, Ticket
from .tokens import account_activation_token
from django.views.generic import ListView
from django.urls import reverse
from urllib.parse import urlencode


#def home_page(request):
#    return render(request, 'main/homepage1.html')
def home_page(request):
    obj = Movie.objects.all()
    smovies = obj.exclude(showtimes__isnull=True)
    cmovies = obj.filter(showtimes__isnull=True)
    #playing = obj.filter()
    #coming =
    #filter(status="published")
    #template_name = 'homepage1.html'
    context = {'smovies': smovies, 'cmovies' : cmovies}
    return render(request, 'main/homepage1.html', context)

def home_page_loggedin(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    obj = Movie.objects.all()
    smovies = obj.exclude(showtimes__isnull=True)
    cmovies = obj.filter(showtimes__isnull=True)
    context = {'smovies': smovies, 'cmovies' : cmovies}
    return render(request, 'main/homepage2.html', context)

def search_bar(request):
    if request.method == "GET":
        #print(request.POST)
        search = request.GET.get('search')
        #print(search)
        submitbutton = request.GET.get('submit')
        if search is not None:
            lookups= Q(title__icontains=search) | Q(category__icontains=search)
            post = Movie.objects.all().filter(lookups)
            smovies = post.exclude(showtimes__isnull=True)
            cmovies = post.filter(showtimes__isnull=True)
            context={'smovies': smovies, 'cmovies' : cmovies, 'submitbutton': submitbutton}
        #print(post)
            return render(request, 'main/search.html', context)
        else:
            return render(request, 'main/search.html')
    else:
        return render(request, 'main/search.html')

def movie_info(request, slug):
    context = {}
    movie = get_object_or_404(Movie, slug=slug)
    shows = movie.showtimes.all()
    context = {'movie': movie, 'shows': shows}
    return render(request, 'main/movie_info.html', context)

def coming_soon(request):
    context = {}
    obj = Movie.objects.all()
    movies = obj.filter(showtimes__isnull=True)
    context = {'movies' : movies}
    return render(request, 'main/coming_soon.html', context)

def action_movie(request):
    context = {}
    movies = Movie.objects.filter(category="action")
    smovies = movies.exclude(showtimes__isnull=True)
    cmovies = movies.filter(showtimes__isnull=True)
    context = {'smovies': smovies, 'cmovies' : cmovies}
    return render(request, 'main/action.html', context)

def adventure_movie(request):
    context = {}
    movies = Movie.objects.filter(category="adventure")
    smovies = movies.exclude(showtimes__isnull=True)
    cmovies = movies.filter(showtimes__isnull=True)
    context = {'smovies': smovies, 'cmovies' : cmovies}
    return render(request, 'main/adventure.html', context)

def animation_movie(request):
    context = {}
    movies = Movie.objects.filter(category="animation")
    smovies = movies.exclude(showtimes__isnull=True)
    cmovies = movies.filter(showtimes__isnull=True)
    context = {'smovies': smovies, 'cmovies' : cmovies}
    return render(request, 'main/animation.html', context)

def comedy_movie(request):
    context = {}
    movies = Movie.objects.filter(category="comedy")
    smovies = movies.exclude(showtimes__isnull=True)
    cmovies = movies.filter(showtimes__isnull=True)
    context = {'smovies': smovies, 'cmovies' : cmovies}
    return render(request, 'main/comedy.html', context)

def drama_movie(request):
    context = {}
    movies = Movie.objects.filter(category="drama")
    smovies = movies.exclude(showtimes__isnull=True)
    cmovies = movies.filter(showtimes__isnull=True)
    context = {'smovies': smovies, 'cmovies' : cmovies}
    return render(request, 'main/drama.html', context)

def scifi_movie(request):
    context = {}
    movies = Movie.objects.filter(category="sci-fi")
    smovies = movies.exclude(showtimes__isnull=True)
    cmovies = movies.filter(showtimes__isnull=True)
    context = {'smovies': smovies, 'cmovies' : cmovies}
    return render(request, 'main/scifi.html', context)

def thriller_movie(request):
    context = {}
    movies = Movie.objects.filter(category="thriller")
    smovies = movies.exclude(showtimes__isnull=True)
    cmovies = movies.filter(showtimes__isnull=True)
    context = {'smovies': smovies, 'cmovies' : cmovies}
    return render(request, 'main/thriller.html', context)


def book_ticket(request, slug):
    if not request.user.is_authenticated:
        return redirect('login_page')
    context = {}
    showtime = get_object_or_404(ShowTime, slug=slug)
    if request.method == 'POST':
        b_form = BookingForm(request.POST)
        if b_form.is_valid():
            Booking = b_form.save(commit=False)  
            Booking.number_adult = b_form.cleaned_data.get('number_adult')
            Booking.number_child = b_form.cleaned_data.get('number_child')
            Booking.number_senior = b_form.cleaned_data.get('number_senior')
            Booking.showtime = get_object_or_404(ShowTime, slug=slug)
            Booking.user = User.objects.get(pk=request.user.id)
            Booking.save()
            booking = Booking
            base_url = reverse('book_seat', kwargs={'slug': slug})  # 1 /products/
            query_string =  urlencode({'booking': booking})  # 2 category=42
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url, slug=slug)
            #return redirect('book_seat', slug=slug)
    else:
        b_form = BookingForm()  
    context = {'b_form': b_form, 'showtime': showtime}
    return render(request, 'main/tickets.html', context)

def book_seat(request, slug):
    context = {}
    showtime = get_object_or_404(ShowTime, slug=slug)
    tickets = Ticket.objects.filter(showtime=showtime)
    bookingid = request.GET.get('booking')
    bookingvar = Booking.objects.get(booking_id = bookingid)
    number_seats = bookingvar.number_tickets()
    if request.method == 'POST':
        #in html action: /seats/{{show.slug}}/?booking={{bookingid}}
        check_values = request.POST.getlist('tag')
        print(check_values)
        if len(check_values) == number_seats:
            return redirect('checkout')
        #if submitbutton:
            #return redirect('checkout')
            #checked_tickets = Ticket.objects.filter(id=request.POST.filter('ticket_id'))
    #print(f'{bookingvar} is null?')
    #card = PaymentCard.objects.filter(user=request.user)
    #booking = Booking.objects.filter(user=request.user, showtime=showtime)
    #data = booking
    #context = {'booking': booking}
    context = {'tickets': tickets, 'booking': bookingvar, 'number_seats': number_seats, 'show': showtime, 'bookingid': bookingid}
    return render(request, 'main/seats.html', context)

def checkout(request):
    return render(request, 'main/checkout.html')

''' 
   if request.method == 'POST':
        b_form = BookingForm(request.POST)
        t_form = TicketForm(request.POST)
        if b_form.is_valid() and t_form.is_valid():
            Booking = b_form.save(commit=False)
            Booking.number_tickets = b_form.cleaned_data.get('number_tickets')
            Booking.booking_status = "active"
            #PaymentCard.expiration_date = form.cleaned_data.get(
            #    'expiration_date')
            #Booking.user = User.objects.get(pk=request.user.id)
            Booking.save()
            Ticket = t_form.save(commit=False)
            Ticket.ticket_type = b_form.cleaned_data.get('ticket_type')
            Ticket.booking = Booking
            Ticket.save()
            return redirect('booking_movie')
    else:
        b_form = BookingForm()
        t_form = TicketForm()
    context = {'b_form': b_form, 't_form' : t_form}
    return render(request, 'main/book_movie.html', context)

def edit_profile_page(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    if request.method == 'POST':
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your Profile has been updated!')
            return redirect('profile_page')
    else:
        current_user = request.user
        current_profile = request.user.profile
        p_form = ProfileUpdateForm(
            initial={'phone_number': current_profile.phone_number, 'address': current_profile.address,
                     'promotions': current_profile.promotions}, instance=request.user)
        u_form = UserUpdateForm(initial={'first_name': current_user.first_name, 'last_name': current_user.last_name},
                                instance=request.user.profile)

    context = {'p_form': p_form, 'u_form': u_form}
    return render(request, 'main/edit_profile.html', context)
'''
def book_movie(request, slug):
    context = {}
    movie = get_object_or_404(Movie, slug=slug)
    shows = movie.showtimes.all()
    context = {'movie': movie, 'shows': shows}
    return render(request, 'main/book_movie.html', context)



'''
def movie_info(request, primary_key):
    try:
        movie = Movie.objects.get(pk=primary_key)
    except Movie.DoesNotExist:
        raise Http404('Movie does not exist')

    return render(request, 'main/movie_info.html', context={'movie': movie})

class SearchResultsView(ListView):
    model = Movie
    template_name = "main/search.html"

    def get_queryset(self): # new
        result = super(SearchResultsView, self).get_queryset()
        query = self.request.GET.get("search")
        print(query)
        if query:
            object_list = Movie.objects.filter(
                Q(title__icontains=query) | Q(category__icontains=query)
            )
        else:
            result = None
        return result
'''
def activation_sent_view(request):
    return render(request, 'main/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'main/activation_invalid.html')


def registration_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.profile.address = form.cleaned_data.get('address')
            user.profile.promotions = form.cleaned_data.get('promotions')
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            message = render_to_string('main/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')
    else:
        form = RegistrationForm()
    return render(request, 'main/signup.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home2')
        else:
            messages.success(request, ("error while login, please try again"))
            return redirect('login_page')
    else:
        return render(request, 'main/loginpage.html', {})


def profile_page(request):  # Fetching data from DB to show user's complete profile page
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(request.POST)
            delete_card = PaymentCard.objects.filter(id=request.POST.get('card_id'))
            delete_card.delete()
    else:
        return redirect('login_page')
    form = RegistrationForm()
    data = request.user.profile
    card = PaymentCard.objects.filter(user=request.user)
    context = {'form': form, 'data': data, 'card': card}
    return render(request, 'main/myprofilepage.html', context)


def edit_profile_page(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    if request.method == 'POST':
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your Profile has been updated!')
            return redirect('profile_page')
    else:
        current_user = request.user
        current_profile = request.user.profile
        p_form = ProfileUpdateForm(
            initial={'phone_number': current_profile.phone_number, 'address': current_profile.address,
                     'promotions': current_profile.promotions}, instance=request.user)
        u_form = UserUpdateForm(initial={'first_name': current_user.first_name, 'last_name': current_user.last_name},
                                instance=request.user.profile)

    context = {'p_form': p_form, 'u_form': u_form}
    return render(request, 'main/edit_profile.html', context)


def add_payment(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            PaymentCard = form.save(commit=False)
            PaymentCard.card_number = form.cleaned_data.get('card_number')
            PaymentCard.expiration_date = form.cleaned_data.get(
                'expiration_date')
            PaymentCard.user = User.objects.get(pk=request.user.id)
            PaymentCard.save()

            return redirect('profile_page')
    else:
        form = PaymentForm()
    return render(request, 'main/add_payment.html', {'form': form})


def logout_page(response):
    logout(response)
    messages.info(response, "Logged out successfully!")
    return redirect('home')
