from django.urls import path

from geoapp import views

urlpatterns = [
    # geo
    path('create/', views.GeoCreateView.as_view()),
    path('list/', views.GeoListView.as_view()),
    path('<int:id>/update/', views.GeoUpdateView.as_view()),
    path('<int:id>/delete/', views.GeoDeleteView.as_view()),
    ]
