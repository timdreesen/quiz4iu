from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
from .models import Question,Category
from forms import CreateNewList,CreateNewQuestion,QuestionEdit



# Create your views here.
def homepage(request):
    return render(request,'homepage.html')

def say_hello(request):
    return render(request,'hello.html', { 'name':'Aleksei'})
    #return HttpResponse('Hello World')

def question_list(request):
    questions = Question.objects.all().order_by('date')
    return render(request, 'question_list.html', {'questions':questions})

def create_category(request):
    if request.method == "GET":
        form = CreateNewList(request.GET)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = Category(name=n)
            t.save()
    else:
        form = CreateNewList()
    return render(request, "create_category.html", {"form":form})

def create_question(request):
    if request.method == "GET":
        form = CreateNewQuestion(request.GET)
        if form.is_valid():
            c = form.cleaned_data["category"]
            n = form.cleaned_data["name"]
            q = form.cleaned_data["question"]
            ac= form.cleaned_data["answer_correct"]
            aw= form.cleaned_data["answer_wrong_1"]
            ar= form.cleaned_data["answer_reason_1"]
            t = Question(category=c,name=n,question=q,answer_correct=ac,answer_wrong_1=aw,answer_reason_1=ar)
            t.save()
    else:
        form = CreateNewQuestion()
    return render(request, "create_question.html", {"form":form})

def question_edit(response,id):
    print(id)
    initial_dict = {
        "category" : Question.objects.get(id=id).category,
        "name" : Question.objects.get(id=id).name,
        "question": Question.objects.get(id=id).question,
        "answer_correct": Question.objects.get(id=id).answer_correct,
        "answer_wrong_1": Question.objects.get(id=id).answer_wrong_1,
        "answer_reason_1": Question.objects.get(id=id).answer_reason_1,
    }
    print(initial_dict)
    qObject = Question.objects.get(id=id)
    if response.method == "GET":
        form = QuestionEdit(response.GET,initial=initial_dict)
        if form.is_valid():
            c = form.cleaned_data["category"]
            n = form.cleaned_data["name"]
            q = form.cleaned_data["question"]
            ac= form.cleaned_data["answer_correct"]
            aw= form.cleaned_data["answer_wrong_1"]
            ar= form.cleaned_data["answer_reason_1"]
            t = Question.objects.get(id=id)
            t.category = c
            t.name = n
            t.question = q
            t.answer_correct = ac
            t.answer_wrong_1 = aw
            t.answer_reason_1 = ar
            t.save()
    else:
        form = CreateNewQuestion()
        print("Failed - 1 ====================================\n")
    return render(response,"question_edit.html",{"form":form})
