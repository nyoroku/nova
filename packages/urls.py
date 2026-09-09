from django.urls import path
from . import views

app_name = 'packages'

urlpatterns = [
    path('', views.PackageListView.as_view(), name='package_list'),
    path('<slug:slug>/', views.PackageDetailView.as_view(), name='package_detail'),
    path('<slug:slug>/quote-partial/', views.PackageQuotePartialView.as_view(), name='quote_partial'),
]
