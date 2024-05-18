from django.urls import path
from authentication.views import login, logout_view, register


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
]
