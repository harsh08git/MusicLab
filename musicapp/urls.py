from unicodedata import name
from django.urls import path ,re_path
from . import views


urlpatterns = [
    path('', views.landing, name='landing'),
    path('account/' , views.index , name='index'),
    path('account/rec/',views.response,name='response'),
    path('genre/<given_genre>',views.genre,name='genre'),
    path('search/<song>',views.fetch,name='fetch'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logoutuser,name='logout')
    # path('response/' , views.response , name='response')
]
