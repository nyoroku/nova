from django.urls import path
from . import views, machine_views

app_name = 'seo'

urlpatterns = [
    path('robots.txt', views.robots_txt, name='robots'),
    path('llms.txt', machine_views.llms_txt, name='llms_txt'),
    path('llms-full.txt', machine_views.llms_full_txt, name='llms_full_txt'),
    path('.well-known/ai-catalog.json', machine_views.ai_catalog_json, name='ai_catalog_json'),
    path('activities/index.json', machine_views.activities_index_json, name='activities_index_json'),
    path('activities/<slug:slug>.json', machine_views.activity_detail_json, name='activity_detail_json'),
    path('activities/<slug:slug>.md', machine_views.activity_detail_md, name='activity_detail_md'),
    path('boat-rides/<slug:slug>.md', machine_views.activity_detail_md, name='boat_ride_detail_md'),
    path('boat-rides.md', machine_views.boat_rides_hub_md, name='boat_rides_hub_md'),
    path('prices.md', machine_views.prices_hub_md, name='prices_hub_md'),
    path('services.md', machine_views.services_hub_md, name='services_hub_md'),
    path('questions.md', machine_views.questions_hub_md, name='questions_hub_md'),
    path('hotel-boat-rides.md', machine_views.hotel_hub_md, name='hotel_hub_md'),
    path('journal/<slug:slug>.md', machine_views.journal_detail_md, name='journal_detail_md'),
]

