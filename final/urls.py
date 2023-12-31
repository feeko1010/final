"""
URL configuration for APIExamples project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from ticketmaster import views
from ticketmaster.views import add_to_favorites, remove_from_favorites

urlpatterns = [
    path("", views.search, name="events"),
    path("events/", views.search, name="events"),
    path("favorites/", views.favorites, name="favorites"),
    path("add_to_favorites/", add_to_favorites, name="add_to_favorites"),
    path("remove_from_favorites/", remove_from_favorites, name="remove_from_favorites"),
]
