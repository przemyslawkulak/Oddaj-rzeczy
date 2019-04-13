"""Oddaj_rzeczy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from app.views import LandingPageView, LoginView, LogoutView, RegisterView, ProfileView, Donate1View, Donate2View, \
    Donate3View, Donate4View, Donate5View, Donate6View, Donate7View, AddOrganizationView, ProfileUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('accounts/login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profileupdate/', ProfileUpdateView.as_view(), name='profile_update'),
    path('donate/', Donate1View.as_view(), name='donate1'),
    path('donate2/', Donate2View.as_view(), name='donate2'),
    path('donate3/', Donate3View.as_view(), name='donate3'),
    path('donate4/', Donate4View.as_view(), name='donate4'),
    path('donate5/', Donate5View.as_view(), name='donate5'),
    path('donate6/', Donate6View.as_view(), name='donate6'),
    path('donate7/', Donate7View.as_view(), name='donate7'),
    path('add-organization/', AddOrganizationView.as_view(), name='add-organization')

]
