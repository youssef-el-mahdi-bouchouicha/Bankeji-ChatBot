from django.urls import path,include 
from . import views 

urlpatterns = [
    path('login',views.login,name='login'),
    path('face_recog',views.face_recog,name='face_recog'),
    path('test',views.test,name='test'),
    path('home',views.home,name='home'),
    path('index',views.index,name='index'),
    path('index2',views.index2,name='index2'),
    path('results',views.results,name='results'),
    
       
]
