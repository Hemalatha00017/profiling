from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('match/', views.match_profiles, name='match_profiles'),
    path('download/', views.download_pdf, name='download_pdf'),
]
