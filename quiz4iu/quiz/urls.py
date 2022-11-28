from django.urls import path
from . import views
from .views import *

#URLconf
urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('question_list/',views.question_list),
    path('',views.homepage,name="home"),
    path('create_question/', views.create_question, name="create_question"),
    path('update_question/<int:pk>/', views.update_question, name="update_question"),
    path('delete_question/<int:pk>/', views.delete_question, name="delete_question"),
    # path('create_room/', views.create_room, name="create_room"),
    # path('update_room/<int:pk>/', views.update_room, name="update_room"),
    # path('delete_room/<int:pk>/', views.delete_room, name="delete_room"),
    # path('delete_message/<int:pk>/', views.delete_message, name="delete_message"),
    path('create_lobby/', views.create_lobby, name="create_lobby"),
    path('lobby/<int:pk>/', views.lobby, name="lobby"),
    path('lobby_msg/<int:pk>/', views.lobby_msg, name="lobby_msg"),
    path('join_lobby/<int:pk>/', views.join_lobby, name="join_lobby"),
    path('leave_lobby/<int:pk>/', views.leave_lobby, name="leave_lobby"),
    path('start_lobby/<int:pk>/', views.start_lobby, name="start_lobby"),
    path('create_category/', views.create_category, name="create_category"),
    
    #überflüssig?
    path('fragenkatalog/',views.fragenkatalog, name="fragenkatalog"),
    
    path('category_catalog/<int:category_id>/',views.category_catalog, name="category_catalog"),
    path('llv/',views.llv, name="llv"),
    path('categorylist/',views.categorylist, name="categorylist"),
    
    path('lobbyinfo/<int:pk>/', views.lobby_refresh, name="lobby_refresh"),
    path('lobbyinfo2/<int:pk>/', views.lobby_refresh2, name="lobby_refresh2"),
    path('create_question_defaultcategory/<int:pk>/', views.create_question_defaultcategory, name="create_question_defaultcategory"),
    path('delete_category/<int:pk>/', views.delete_category, name="delete_category"),
    #path('ajax_view/<int:pk>/', views.ajax_view, name='ajax_view'),
    
    path('impressum/',views.impressum, name="impressum"),
    path('bestenliste/',views.bestenliste, name="bestenliste"),

    #path("<int:id>",views.index, name="index"),
    #path('room/<int:pk>/', views.room, name="room"),
]