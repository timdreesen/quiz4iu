from django.urls import path
from . import views

#URLconf
urlpatterns = [
    path('hello/',views.say_hello),
    path('question_list/',views.question_list),
    path('',views.homepage),
]