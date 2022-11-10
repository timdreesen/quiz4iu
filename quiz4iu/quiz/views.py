from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpRequest
from .models import Question,Category,Room
from forms import CreateNewList,CreateNewQuestion,QuestionForm



# Create your views here.
def homepage(request):
    rooms = Room.objects.all().order_by('id')
    questions = Question.objects.all().order_by('date')
    return render(request,'homepage.html', {'rooms':rooms,'questions':questions})

def say_hello(request):
    return render(request,'hello.html', { 'name':'Aleksei'})
    #return HttpResponse('Hello World')

def question_list(request):
    questions = Question.objects.all().order_by('date')
    return render(request, 'question_list.html', {'questions':questions})

def create_category(request):
    if request.method == "POST":
        form = CreateNewList(request.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = Category(name=n)
            t.save()
    else:
        form = CreateNewList()
    return render(request, "create_category.html", {"form":form})

def index(request,id):
    q = Question.objects.get(id=id)
    print(request)
    return render(request, 'one_question.html', {'question':q})

def index2(request,id):
    q = Question.objects.get(id=id)
    return render(request, 'one_question.html', {'question':q})



def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'room.html', context)

def create_question(request):
    form = QuestionForm()
    if request.method == "POST":
        #print(request.POST)
        #request.POST.get('name')....
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'question_form.html',context)

def update_question(request,pk):
    question = Question.objects.get(id=pk)
    form = QuestionForm(instance=question)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'question_form.html',context)

def delete_question(request,pk):
    question = Question.objects.get(id=pk)
    if request.method == "POST":
        question.delete()
        return redirect('home')
    return render(request,"delete.html", {'obj':question})

