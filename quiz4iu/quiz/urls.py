from django.urls import path,include
from . import views

#URLconf
urlpatterns = [
    path('hello/',views.say_hello),
    path('question_list/',views.question_list),
    path('',views.homepage),
    path("create_category/", views.create_category, name="create_category" ),
    path("create_question/", views.create_question, name="create_question"),
    path("question_edit/<int:id>", views.question_edit, name="question_edit"),
    #path("<int:id>",views.question_edit, name="index"),
]