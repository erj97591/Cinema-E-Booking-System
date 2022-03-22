from django.contrib import admin
from django.urls import path
from .views import registration_page, home_page, activation_sent_view, activate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name="home"),
    path('register/', registration_page, name="register"),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    ]