from django.urls import path

from . import views

app_name = 'guess'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/detail/', views.GameView.as_view(), name='detail'),
    path('new/', views.new_game, name='new_game'),
    path('<int:game_id>/guess/', views.new_guess, name='new_guess'),
    path('<int:pk>/inspect/', views.InspectView.as_view(), name='inspect'),
]
