from django.urls import path
from . import views
from django.contrib import admin
from main import views as main_views
urlpatterns = [
path("home/<int:id>", views.home, name = "home"),
path("login/", views.login_page, name = "login_page"),
path("register/", views.registration_page, name = "registration_page"),
path("admin/", admin.site.urls),
]