from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<user_id>/insert/', views.insert, name='insert'),
    # ex: /polls/5/results/
    path('<user_id>/update/', views.update, name='update'),
    # ex: /polls/5/vote/
    path('<user_id>/delete/', views.delete, name='delete')
]