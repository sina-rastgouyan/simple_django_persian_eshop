from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContactUsView.as_view(), name='contact_us_page'),
    path('create-profile/', views.TestUserProfile.as_view(), name='profile_page'),
]
