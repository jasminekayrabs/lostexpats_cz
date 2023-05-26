from django.urls import path
from authentication import views

"""renders signup and login functions specified in views.py"""
urlpatterns = [
    path("", views.home, name="home"),
    path("signup", views.render_signup, name="render_signup"),
    path("login", views.render_login, name="render_login"),
    path('logout', views.logout_view, name='logout'),
    path("fooddrinks", views.render_fooddrinks, name="render_fooddrinks"),
    path("nightlife", views. render_nightlife, name="render_nightlife"),
    path("news", views.render_news, name="render_news"),
    path("events", views.render_events, name="render_events"),
    path("index", views.render_index, name="render_index"),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate_account'),
    path('activation_sent/', activation_sent, name='activation_sent'),
    path("terms", render_terms, name="render_terms"),
]

