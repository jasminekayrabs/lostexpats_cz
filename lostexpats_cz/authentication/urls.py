from django.urls import path
from authentication import views
from .views import activate_account, activation_sent, render_terms, CustomPasswordResetView
from .views import save_cookie_consent
from .views import save_cookie_preferences
from .views import (
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)


"""renders signup and login functions specified in views.py"""
urlpatterns = [
    path("", views.home, name="home"),
    path("signup", views.render_signup, name="render_signup"),
    path("login", views.render_login, name="render_login"),
    path('login/', views.render_login, name='login'),
    path('logout', views.logout_view, name='logout'),
    path("fooddrinks", views.render_fooddrinks, name="render_fooddrinks"),
    path("nightlife", views. render_nightlife, name="render_nightlife"),
    path("news", views.render_news, name="render_news"),
    path("events", views.render_events, name="render_events"),
    path("index", views.render_index, name="render_index"),
    path('reset_password/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
    path('activation_sent/', activation_sent, name='activation_sent'),
    path("terms", render_terms, name="render_terms"),
    path('secure/', views.secure_view, name='secure_view'),
    path('save-cookie-preferences/', save_cookie_preferences, name='save_cookie_preferences'),
    path('save-cookie-consent/', save_cookie_consent, name='save_cookie_consent'),
]

