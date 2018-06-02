from django.conf.urls import url
from . import views

urlpatterns = [
    url("^$", views.index, name="index"),
    url("^process/$", views.process, name="process"),
    url("^start/$", views.start, name="start"),
    url("^signup/$", views.signup, name="signup"),
    url("^leaderboard/$", views.leaderboard, name="leaderboard"),
]
