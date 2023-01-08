from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length = 100)
    question = models.TextField()
    answer_correct = models.CharField(max_length = 100)
    answer_wrong_1 = models.CharField(max_length = 100)
    #answer_wrong_2 = models.CharField(max_length = 100)
    #answer_wrong_3 = models.CharField(max_length = 100)
    answer_reason_1 = models.CharField(max_length = 100)
    #answer_reason_2 = models.CharField(max_length = 100)
    #answer_reason_3 = models.CharField(max_length = 100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def snippet(self):
        return self.question[:10] + "..."

class Lobby(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    participants = models.ManyToManyField(User, related_name='participantslobby', blank=True)
    max_players = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.IntegerField()
    questions = models.ManyToManyField(Question, blank=True)


#    def __init__(self,host,name,max_players,category):
#        self.id = next(Lobby.id_obj)
#        self.host = host
#        self.name = name
#        self.participants = [host,]
#        self.max_players = max_players
#        self.category = category
#        self.status = 0
#        questions = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

#    test  class
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body


#Database independent classes



