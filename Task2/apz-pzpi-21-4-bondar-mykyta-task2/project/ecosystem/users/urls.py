from django.urls import path

from locations.views import create_location, payment_success
from users.views import login, registration, profile, settings, logout

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('settings/', settings, name='settings'),
    path('logout/', logout, name='logout'),
    path('create_location/', create_location, name='create_location'),
    path('payment_success', payment_success, name='payment_success'),
]