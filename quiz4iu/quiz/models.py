from email.policy import default
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True, null=True)
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

