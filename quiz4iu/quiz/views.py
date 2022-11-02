from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

# Create your views here.
def homepage(request):
    return render(request,'homepage.html')

def say_hello(request):
    return render(request,'hello.html', { 'name':'Aleksei'})
    #return HttpResponse('Hello World')

def question_list(request):
    questions = Question.objects.all().order_by('date')
    return render(request, 'question_list.html', {'questions':questions})