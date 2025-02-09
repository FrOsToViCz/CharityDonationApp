"""
URL configuration for CharityDonationApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from charity.views import LandingPage, AddDonation, Login, Register, FormConfirmation, UserProfile, ChangePassword, \
    UserSettings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name='landing-page'),
    path('add-donation/', AddDonation.as_view(), name='add-donation'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing-page'), name='logout'),
    path('add-donation/form-confirmation/', FormConfirmation.as_view(), name='form-confirmation'),
    path('profile/', UserProfile.as_view(), name='user-profile'),
    path('settings/', UserSettings.as_view(), name='user-settings'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
]
