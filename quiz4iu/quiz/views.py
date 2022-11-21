from time import time
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from forms import CreateNewList, QuestionForm, RoomForm, LobbyForm, QuestionFormDefaultCategory

#AJAX
from django.http import JsonResponse
from django.core import serializers
from django.views.generic import View
import json

from .models import Category, Question, Room, Topic, Message, Lobby


    
def fragenkatalog(request):
    questions = Question.objects.all().order_by('date')

    return render(request, 'fragenkatalog.html', {'questions':questions})

def category_catalog(request,category_id):
    category = Category.objects.get(id=category_id)
    questions = Question.objects.filter(category=category)
    context = {'questions':questions, 'category':category}
    return render(request,'fragenkatalog.html',context)

def categorylist(request):
    questions = Question.objects.all().order_by('date')
    categories = Category.objects.all().order_by('id')
    context = {'categories':categories, 'questions':questions}
    return render(request, 'categorylist.html', context)


# Create your views here.
def lobby(request,pk):
    lobby = Lobby.objects.get(id=pk)
    if request.method == 'POST':
        print(request.POST)
        questions = lobby.questions.all()
        score=0
        wrong=0
        correct=0
        total=0
        for q in questions:
            total+=1
            print(request.POST.get(q.question))
            print(q.answer_correct)
            print()
            if q.answer_correct ==  request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                wrong+=1
        percent = score/(1+total*10) *100
        lobby.delete()
        context = {
            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total
        }
        return render(request,'result.html',context)
    else:
        participants = lobby.participants.all()
        context = {'lobby':lobby,'participants':participants, 'questions':lobby.questions.all()}
        print(participants)
        return render(request,'lobby.html',context)

    
@login_required(login_url='login')
def create_lobby(request):
    form = LobbyForm()
    if request.method == "POST":
        #print(request.POST)
        #request.POST.get('name')....
        form = LobbyForm(request.POST)
        if form.is_valid():
            lobbyname = form.cleaned_data["name"]
            lobbymax_players = form.cleaned_data["max_players"]
            lobbycategory = form.cleaned_data["category"]
            lobby = Lobby(host=request.user,name=lobbyname,max_players=lobbymax_players,category=lobbycategory,status=0)
            lobby.save()
            lobby.participants.add(request.user)
            lobby.save()
            return redirect('lobby',pk=lobby.id)
            #return redirect('home')
        else:
            form = LobbyForm()

    context = {'form':form}
    return render(request,'question_form.html',context)

def join_lobby(request,pk):
    lobby = Lobby.objects.get(id=pk)
    lobby.participants.add(request.user)
    lobby.save()
    participants = lobby.participants.all()
    context = {'lobby':lobby,'participants':participants}
    return render(request,'lobby.html',context)

def leave_lobby(request,pk):
    lobby = Lobby.objects.get(id=pk)
    lobby.participants.remove(request.user)
    participants = lobby.participants.all()
    lobby.save()
    if len(participants)==0:
        lobby.delete()
        return redirect('home')
    context = {'lobby':lobby,'participants':participants}
    return render(request,'lobby.html',context)

def start_lobby(request,pk):
    lobby = Lobby.objects.get(id=pk)
    if lobby.status == 0:
        lobby.status = 1
        #achtung oder_by('?') wohl sehr langsam
        items = Question.objects.filter(category=lobby.category).order_by('?')[:5]
        for i in items:
            lobby.questions.add(i)
        lobby.save()
        print(lobby.status)
        for q in lobby.questions.all():
            print(q)
    questions = lobby.questions.all()
    context ={'lobby':lobby,'questions':questions}
    return render(request,'lobby.html',context)

# Create your views here.
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            #adds user into the session
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page':page}
    return render(request,'login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    #page = 'register'
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')

    return render(request,'login_register.html',{'form':form})

def homepage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    #rooms = Room.objects.all().filter(
    #    Q(topic__name__icontains=q) |
    #    Q(name__icontains=q)        |
    #    Q(description__icontains=q) |
    #    Q(host__username__icontains=q)
    #    )
    categories = Category.objects.all().order_by('id')
    LobbyList = Lobby.objects.all()
    context = {'categories':categories,'lobbylist':LobbyList}
    return render(request,'homepage.html', context)


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
            return redirect('category_catalog', category_id=t.id)
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
    room_messages = room.message_set.all().order_by('-date')
    particitpants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)


    context = {'room':room, 'room_messages':room_messages, 'particitpants':particitpants}
    return render(request, 'room.html', context)

@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'room_form.html',context)

@login_required(login_url='login')
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'room_form.html',context)

@login_required(login_url='login')
def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request,"delete.html", {'obj':room})  

@login_required(login_url='login')
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

@login_required(login_url='login')
def create_question_defaultcategory(request, pk):
    print('name\n')
    print("------")
    print("name\n")
    form = QuestionFormDefaultCategory()
    if request.method == "POST":
        #print(request.POST)
        #request.POST.get('name')....
        form = QuestionFormDefaultCategory(request.POST)
        if form.is_valid():
            questioncategory = Category.objects.get(id=pk)
            questionname = form.cleaned_data["name"]
            questionquestion = form.cleaned_data["question"]
            questionanswer_correct = form.cleaned_data["answer_correct"]
            questionanswer_wrong_1 = form.cleaned_data["answer_wrong_1"]
            questionanswer_reason_1 = form.cleaned_data["answer_reason_1"]
            question = Question(category=questioncategory, name=questionname, question=questionquestion, answer_correct=questionanswer_correct, answer_wrong_1=questionanswer_wrong_1, answer_reason_1=questionanswer_reason_1 )
            question.save()
            return redirect('category_catalog',category_id=pk)
        
    context = {'form':form}
    return render(request,'question_form.html',context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def delete_question(request,pk):
    question = Question.objects.get(id=pk)
    if request.method == "POST":
        question.delete()
        return redirect('home')
    return render(request,"delete.html", {'obj':question})

@login_required(login_url='login')
def delete_category(request,pk):
    category = Category.objects.get(id=pk)
    if request.method == "POST":
        category.delete()
        return redirect('categorylist')
    return render(request,"delete.html", {'obj':category})


@login_required(login_url='login')
def delete_message(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request,"delete.html", {'obj':message})


#AJAX

def llv(request):
    LobbyList = Lobby.objects.all()
    context = {'lobbylist':LobbyList}
    return render(request,'lobbylist.html', context)

def lobby_refresh(request,pk):
    lobby = Lobby.objects.get(id=pk)
    print("lobby refreshed!")
    #context = {"lobbyname":lobby.name,'lobbyid':lobby.id, "lobbystatus":lobby.status}
    context = {'lobby':lobby,'participants':lobby.participants.all(), 'questions':lobby.questions.all()}
    #return JsonResponse(context)
    return render(request,'lobbyinfo.html',context)


def is_ajax(request):
     return request.headers.get('x-requested-with') == 'XMLHttpRequest'



#AJAX TUTORIAL 

# def get(request):
#     text = request.GET.get('div_inhalt')

#     print()
#     print("div inhalt wurde abgefragt (view)")
#     print()
        
#     if is_ajax(request):
#         t = time()
#         return JsonResponse({text}, status=200)
            
#     return render(request,'homepage.html')


# class AjaxHandlerView(View):
#     def get(self, request):
#         text = request.GET.get('button_text')

#         print()
#         print(text)
#         print()
        
#         if is_ajax(request):
#             t = time()
#             return JsonResponse({'seconds': t,}, status=200)
            
#         return render(request,'homepage.html')
    
#     def post(self, request):
        
#         card_text = request.POST.get('text')
        
#         result = f"clicked {card_text}"
        
#         if is_ajax(request):
#             return JsonResponse({'data': result}, status=200)
        
#         return render(request,'homepage.html')
    