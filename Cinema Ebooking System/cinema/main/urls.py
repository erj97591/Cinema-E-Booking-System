from django.urls import path
from . import views
urlpatterns = [
path("home/<int:id>", views.home, name = "home"),
path("login/", views.login_page, name = "login_page"),
]