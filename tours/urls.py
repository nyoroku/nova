from django.urls import path
from . import views

app_name = 'tours'

urlpatterns = [
    path('', views.TourListView.as_view(), name='tour_list'),
    path('<slug:slug>/', views.TourDetailView.as_view(), name='tour_detail'),
    path('<slug:slug>/quote-partial/', views.TourQuotePartialView.as_view(), name='quote_partial'),
]
