from django import forms
from django.db import models
from django.forms import ModelForm

from quiz.models import Question,Category,Room

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    check = forms.BooleanField(required=False)

class CreateNewQuestion(forms.Form):
    category = forms.ModelChoiceField(required=False,widget=forms.Select, queryset=Category.objects.all())
    name = forms.CharField(label="Name", max_length=200)
    question = forms.CharField(label="Question", max_length=200)
    answer_correct = forms.CharField(label="Correct Answer", max_length=200)
    answer_wrong_1 = forms.CharField(label="Wrong Answer 1", max_length=200)
    answer_reason_1 = forms.CharField(label="Reason 1", max_length=200)

# class QuestionEdit(forms.Form):
#     category = forms.ModelChoiceField(required=False,widget=forms.Select, queryset=Category.objects.all())
#     name = forms.CharField(label="Name", max_length=200)
#     question = forms.CharField(label="Question", max_length=200)
#     answer_correct = forms.CharField(label="Correct Answer", max_length=200)
#     answer_wrong_1 = forms.CharField(label="Wrong Answer 1", max_length=200)
#     answer_reason_1 = forms.CharField(label="Reason 1", max_length=200)
    
class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        #fields = ['name','body',...]

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
