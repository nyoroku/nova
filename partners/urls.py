from django.urls import path
from . import views

app_name = 'partners'

urlpatterns = [
    path('', views.HotelHubView.as_view(), name='hotel_hub'),
    path('check/', views.HotelCheckerPartialView.as_view(), name='hotel_check'),
    path('<slug:slug>/', views.HotelDetailView.as_view(), name='hotel_detail'),
]
