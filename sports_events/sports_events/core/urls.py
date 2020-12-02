from django.urls import path
from sports_events.core import views

urlpatterns = [
	path(r'match/', views.EventsAPI.as_view(),name="all_matches"),
	path(r'match/<id>/', views.EventAPI.as_view(), name="match")
]