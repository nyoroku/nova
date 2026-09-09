from django.urls import path
from . import views

app_name = 'stays'

urlpatterns = [
    path('', views.StayListView.as_view(), name='stay_list'),
    path('<slug:slug>/', views.StayDetailView.as_view(), name='stay_detail'),
]
