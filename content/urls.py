from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.JournalListView.as_view(), name='journal_list'),
    path('<slug:slug>/', views.JournalDetailView.as_view(), name='journal_detail'),
]
