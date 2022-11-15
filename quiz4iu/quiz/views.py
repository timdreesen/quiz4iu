from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from forms import CreateNewList, CreateNewQuestion, QuestionForm

from .models import Category, Question, Room


# Create your views here.
def homepage(request):
    rooms = Room.objects.all().order_by('id')
    questions = Question.objects.all().order_by('date')
    categories = Category.objects.all().order_by('id')
    return render(request,'homepage.html', {'rooms':rooms,'questions':questions, 'categories':categories})

def question_list(request):
    questions = Question.objects.all().order_by('date')
    return render(request, 'question_list.html', {'questions':questions})

def fragenkatalog(request):
    questions = Question.objects.all().order_by('date')
    return render(request, 'fragenkatalog.html', {'questions':questions})

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

# def create_question(request):
#     if request.method == "POST":
#         form = CreateNewQuestion(request.POST)
#         if form.is_valid():
#             c = form.cleaned_data["category"]
#             n = form.cleaned_data["name"]
#             q = form.cleaned_data["question"]
#             ac= form.cleaned_data["answer_correct"]
#             aw= form.cleaned_data["answer_wrong_1"]
#             ar= form.cleaned_data["answer_reason_1"]
#             t = Question(category=c,name=n,question=q,answer_correct=ac,answer_wrong_1=aw,answer_reason_1=ar)
#             t.save()
#     else:
#         form = CreateNewQuestion()
#     return render(request, "create_question.html", {"form":form})

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
        print(request.POST)
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



#def question_edit(request,id):
#    pass
'''
def question_edit(response):
#    print(id)
#    initial_dict = {
#        "category" : Question.objects.get(id=id).category,
#        "name" : Question.objects.get(id=id).name,
#        "question": Question.objects.get(id=id).question,
#        "answer_correct": Question.objects.get(id=id).answer_correct,
#        "answer_wrong_1": Question.objects.get(id=id).answer_wrong_1,
#        "answer_reason_1": Question.objects.get(id=id).answer_reason_1,
#    }
#    print(initial_dict)
    if response.method == "POST":
        form = QuestionEdit(response.POST)
        if form.is_valid():
            c = form.cleaned_data["category"]
            n = form.cleaned_data["name"]
            q = form.cleaned_data["question"]
            ac= form.cleaned_data["answer_correct"]
            aw= form.cleaned_data["answer_wrong_1"]
            ar= form.cleaned_data["answer_reason_1"]
            t = Question.objects.POST(id=id)
            t.category = c
            t.name = n
            t.question = q
            t.answer_correct = ac
            t.answer_wrong_1 = aw
            t.answer_reason_1 = ar
            t.save()
        print("Filled Form - 1 ====================================\n")
    else:
        #form = CreateNewQuestion(initial=initial_dict)
        form = CreateNewQuestion()
        print("New Form - 2 ====================================\n")
    return render(response,"question_edit.html",{"form":form})
'''