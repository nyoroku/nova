from django.urls import path
from . import views
from .operations import operations_overview

app_name = 'bookings'

urlpatterns = [
    path('options/', views.booking_options, name='options'),
    path('operations/', operations_overview, name='operations'),
    path('', views.BookView.as_view(), name='book'),
]
