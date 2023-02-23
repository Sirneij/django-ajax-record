from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("record/", views.record, name="record"),
    path("record/detail/<uuid:id>/", views.record_detail, name="record_detail"),
	path("record/<uuid:id>", views.delete_audio, name="delete_audio"),
]
