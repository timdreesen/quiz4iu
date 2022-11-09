from email.policy import default
from django.db import models

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

#    test  class
class Room(models.Model):
    #host =
    #topic =
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    #participants
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#Database independent classes

class Lobby():
    def __init__(self, name):
        self.name = name
        self.max_players = 5
        self.category = "default_category"
        self.question_count = 5

    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_max_players(self):
        return self.max_players
    def set_max_players(self, max_players):
        self.max_players = max_players
    def get_category(self):
        return self.category
    def set_category(self, category):
        self.category = category
    def get_question_count(self):
        return self.question_count
    def set_question_count(self, question_count):
        self.question_count = question_count

