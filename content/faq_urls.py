from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.FAQView.as_view(), name='faq_list'),
]
