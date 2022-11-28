from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 100, validators=[alphanumeric])

    def __str__(self):
        return self.name

class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, validators=[alphanumeric])
    question = models.TextField(validators=[alphanumeric])
    answer_correct = models.CharField(max_length = 200, validators=[alphanumeric])
    answer_wrong_1 = models.CharField(max_length = 200, validators=[alphanumeric])
    answer_wrong_2 = models.CharField(max_length = 200, validators=[alphanumeric])
    answer_wrong_3 = models.CharField(max_length = 200, validators=[alphanumeric])
    answer_reason_1 = models.CharField(max_length = 200, validators=[alphanumeric])
    answer_reason_2 = models.CharField(max_length = 200, validators=[alphanumeric])
    answer_reason_3 = models.CharField(max_length = 200, validators=[alphanumeric])
    date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.question


class Participant(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.PositiveIntegerField()
    score = models.PositiveIntegerField()
    wrong = models.PositiveIntegerField()
    correct = models.PositiveIntegerField()
    total = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username

class Lobby(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, validators=[alphanumeric])
    participants = models.ManyToManyField(Participant, blank=True)
    max_players = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.PositiveIntegerField()
    questions = models.ManyToManyField(Question, blank=True)



# class Topic(models.Model):
#     name = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name

# #    test  class
# class Room(models.Model):
#     host = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
#     topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)
#     name = models.CharField(max_length=200)
#     description = models.TextField(null=True,blank=True)
#     participants = models.ManyToManyField(User, related_name='participants', blank=True)
#     update = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

# class Message(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     body = models.TextField()
#     date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.body


#Database independent classes



