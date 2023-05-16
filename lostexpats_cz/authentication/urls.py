from django.urls import path
from authentication import views

"""renders signup and login functions specified in views.py"""
urlpatterns = [
    path("", views.home, name="home"),
    path("signup", views.render_signup, name="render_signup"),
    path("login", views.render_login, name="render_login"),
    path("logout", views.render_logout, name="render_logout"),
    path("fooddrinks", views.render_fooddrinks, name="render_fooddrinks"),
    path("nightlife", views. render_nightlife, name="render_nightlife"),
    path("news", views.render_news, name="render_news"),
]

