from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='home'),
    path('signup',signup,name='signup'),
    path('login',Login,name='login'),
    path('logout',Logout,name='logout'),
    path('about',About,name='about'),
    path('contact',Contact,name='contact'),
    path('profile',Profile,name='profile'),
    path('deleteprofile',DeleteProfile,name='deleteprofile'),

]

