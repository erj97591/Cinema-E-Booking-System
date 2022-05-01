from django.contrib import admin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path

from .views import registration_page, home_page, activation_sent_view, activate, login_page, home_page_loggedin, \
    profile_page, logout_page, add_payment, edit_profile_page, search_bar, movie_info, coming_soon, action_movie, adventure_movie, animation_movie, comedy_movie, drama_movie, scifi_movie, thriller_movie, book_movie, book_ticket, book_seat, checkout



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name="home"),
    path('home/', home_page_loggedin, name="home2"),
    path('register/', registration_page, name="register"),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path("login/", login_page, name="login_page"),
    path("logout/", logout_page, name="logout_page"),
    path("profile/", profile_page, name="profile_page"),
    path("editprofile/", edit_profile_page, name="edit_profile_page"),
    path("addpayment/", add_payment, name="add_payment"),
    path("search/", search_bar, name="search_bar"),
    path("action/", action_movie, name="action_movie"),
    path("adventure/", adventure_movie, name="adventure_movie"),
    path("animation/", animation_movie, name="animation_movie"),
    path("comedy/", comedy_movie, name="comedy_movie"),
    path("drama/", drama_movie, name="drama_movie"),
    path("scifi/", scifi_movie, name="scifi_movie"),
    path("thriller/", thriller_movie, name="thriller_movie"),
    path("soon/", coming_soon, name = "coming_soon"),
    path("booking/<slug>/", book_movie, name="book_movie"),
    path("tickets/<slug>/", book_ticket, name="book_ticket"),
    path("seats/<slug>/", book_seat, name="book_seat"),
    path("checkout/<slug>/", checkout, name="checkout"),
    path("<slug>/", movie_info, name="movie_info"),

    #path('movie/<int:pk>', views.MovieDetailView.as_view(), name='movie_info'),
    #path('search/<str:search_info>/', SearchResultsView.as_view(), name = "search_bar"),
    path('password_reset/', PasswordResetView.as_view(
        template_name='main/password/password_reset.html',
        email_template_name='main/password/password_reset_email.html',
        subject_template_name='main/password/password_reset_subject.txt',
        success_url='/password_reset/done/'),
         name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='main/password/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='main/password/password_reset_confirm.html',
        success_url='/reset/done/'),
         name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='main/password/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password_change/', PasswordChangeView.as_view(
        template_name='main/password/password_change.html',
        success_url='password_change_done/'),
         name='password_change'),
    path('password_change/password_change_done/', PasswordChangeDoneView.as_view(
        template_name='main/password/password_change_done.html'),
         name='password_change_done'),
]
