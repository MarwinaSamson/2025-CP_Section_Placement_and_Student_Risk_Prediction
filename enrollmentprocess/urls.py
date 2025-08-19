from django.urls import path
from . import views
urlpatterns = [
        path("", views.homepage, name="homepage"), # Route the root URL to the homepage view
    ]
    