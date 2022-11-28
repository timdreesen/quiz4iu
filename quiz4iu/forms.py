from django import forms
from django.db import models
from django.forms import ModelForm

from quiz.models import Question,Category #,Room

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)

class LobbyForm(forms.Form):
    name = forms.CharField(label="Lobbyname",max_length=200)
    max_players = forms.IntegerField(label="max. Spieler", min_value= 1)
    category = forms.ModelChoiceField(label="Kurs",widget=forms.Select,queryset=Category.objects.all())

class QuestionForm(ModelForm):
    # category = forms.ModelChoiceField(label="Kurs", required=False,widget=forms.Select, queryset=Category.objects.all())
    # question = forms.CharField(label="Frage", max_length=200)
    # answer_correct = forms.CharField(label="richtige Antwort", max_length=200)
    # answer_wrong_1 = forms.CharField(label="falsche Antwort 1", max_length=200)
    # answer_wrong_2 = forms.CharField(label="falsche Antwort 2", max_length=200)
    # answer_wrong_3 = forms.CharField(label="falsche Antwort 3", max_length=200)
    # answer_reason_1 = forms.CharField(label="Begründung 1", max_length=200)
    # answer_reason_2 = forms.CharField(label="Begründung 2", max_length=200)
    # answer_reason_3 = forms.CharField(label="Begründung 3", max_length=200)
    class Meta:
        model = Question
        fields = '__all__'
        # fields = ['name','body',...]
        labels = {
            'category': ('Kurs'),
            'question': ('Frage'),
            'answer_correct': ('richtige Antwort'),
            'answer_wrong_1': ('falsche Antwort 1'),
            'answer_wrong_2': ('falsche Antwort 2'),
            'answer_wrong_3': ('falsche Antwort 3'),
            'answer_reason_1': ('Begründung 1'),
            'answer_reason_2': ('Begründung 2'),
            'answer_reason_3': ('Begründung 3'),
        }
        # help_texts = {
        #     'name': _('Some useful help text.'),
        # }
        # error_messages = {
        #     'name': {
        #         'max_length': _("This writer's name is too long."),
        #     },
        # }
        

class QuestionFormDefaultCategory(forms.Form):
    #name = forms.CharField(label="Name", max_length=200)
    question = forms.CharField(label="Frage", max_length=200)
    answer_correct = forms.CharField(label="richtige Antwort", max_length=200)
    answer_wrong_1 = forms.CharField(label="falsche Antwort 1", max_length=200)
    answer_wrong_2 = forms.CharField(label="falsche Antwort 2", max_length=200)
    answer_wrong_3 = forms.CharField(label="falsche Antwort 3", max_length=200)
    answer_reason_1 = forms.CharField(label="Begründung 1", max_length=200)
    answer_reason_2 = forms.CharField(label="Begründung 2", max_length=200)
    answer_reason_3 = forms.CharField(label="Begründung 3", max_length=200)

# class CreateNewQuestion(forms.Form):
#     category = forms.ModelChoiceField(required=False,widget=forms.Select, queryset=Category.objects.all())
#     name = forms.CharField(label="Name", widget=forms.TextInput, max_length=200)
#     question = forms.CharField(label="Question", max_length=200)
#     answer_correct = forms.CharField(label="Correct Answer", max_length=200)
#     answer_wrong_1 = forms.CharField(label="Wrong Answer 1", max_length=200)
#     answer_reason_1 = forms.CharField(label="Reason 1", max_length=200)

# class RoomForm(ModelForm):
#     class Meta:
#         model = Room
#         fields = '__all__'
    