from django.shortcuts import render
from django.http import HttpResponse
from .models import Question,Category
from forms import CreateNewList,CreateNewQuestion



# Create your views here.
def homepage(request):
    return render(request,'homepage.html')

def say_hello(request):
    return render(request,'hello.html', { 'name':'Aleksei'})
    #return HttpResponse('Hello World')

def question_list(request):
    questions = Question.objects.all().order_by('date')
    return render(request, 'question_list.html', {'questions':questions})

def create_category(response):
    if response.method == "GET":
        form = CreateNewList(response.GET)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = Category(name=n)
            t.save()
    else:
        form = CreateNewList()
    return render(response, "create_category.html", {"form":form})

def create_question(response):
    if response.method == "GET":
        form = CreateNewQuestion(response.GET)
        if form.is_valid():
            n = form.cleaned_data["name"]
            q = form.cleaned_data["question"]
            ac= form.cleaned_data["answer_correct"]
            aw= form.cleaned_data["answer_wrong_1"]
            ar= form.cleaned_data["answer_reason_1"]
            t = Question(name=n,question=q,answer_correct=ac,answer_wrong_1=aw,answer_reason_1=ar)
            t.save()
    else:
        form = CreateNewQuestion()
    return render(response, "create_question.html", {"form":form})
     