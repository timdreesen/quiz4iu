from django.urls import path,include
from . import views

#URLconf
urlpatterns = [
    path('hello/',views.say_hello),
    path('question_list/',views.question_list),
    path('',views.homepage,name="home"),
    path("create_category/", views.create_category, name="create_category" ),
    path("create_question/", views.create_question, name="create_question"),

    #path("question_edit/<int:id>/", views.question_edit, name="question_edit"),
    #path("question_edit/", views.question_edit, name="question_edit"),
    path("<int:id>",views.index, name="index"),
    path('room/<int:pk>/', views.room, name="room"),
    path('create_question/', views.create_question, name="create_question"),
    path('update_question/<int:pk>/', views.update_question, name="update_question"),
    path('delete_question/<int:pk>/', views.delete_question, name="delete_question"),

]