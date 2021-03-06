"""netflixmediafinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
	path('usermovies/', include('usermovies.urls')),
    path('admin/', admin.site.urls),
    # path('users/', views.showdetails),
    # path('adduser/', views.addUser),
    path('register/', views.Register),
    path('login/', views.Login),
    path('newregistration/', views.NewRegistration),
    path('watchlist/', views.Watchlist),
    path('addmovie/', views.AddMovie),
    path('removemovie/', views.RemoveMovie),
    path('searchmovie/', views.SearchMovie),
    path('editrating/', views.EditRating),
    path('', views.Login),
    path('recommendations/', views.Recommendations),
    path('userprofile/', views.UserProfile),

    path('test_agreeableness/', views.Agreeableness),
    path('test_conscientiousness/', views.Conscientiousness),
    path('test_extraversion/', views.Extraversion),
    path('test_neuroticism/', views.Neuroticism),
    path('test_openness/', views.Openness),
    path('updateattribute/', views.UpdateAttribute),
    path('details/<show_id>', views.Details)
]
