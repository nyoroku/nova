from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('prices/', views.PricesView.as_view(), name='prices'),
    path('plan-naivasha/', views.PlanNaivashaView.as_view(), name='plan_naivasha'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
