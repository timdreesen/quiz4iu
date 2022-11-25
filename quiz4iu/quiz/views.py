#from time import time
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
#from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from forms import CreateNewList, QuestionForm, LobbyForm, QuestionFormDefaultCategory #RoomForm,

#AJAX
from django.http import JsonResponse
# from django.core import serializers
# from django.views.generic import View
# import json

from .models import Category, Question, Lobby, Participant # Room, Topic, Message,

import random


    
def fragenkatalog(request):
    questions = Question.objects.all().order_by('date')

    return render(request, 'fragenkatalog.html', {'questions':questions})

def category_catalog(request,category_id):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    #rooms = Room.objects.all().filter(
    #    Q(topic__name__icontains=q) |
    #    Q(name__icontains=q)        |
    #    Q(description__icontains=q) |
    #    Q(host__username__icontains=q)
    #    )

    category = Category.objects.get(id=category_id)
    #questions = Question.objects.filter(category=category)
    questions = Question.objects.filter(category=category).filter(
        Q(question__icontains=q)   
    )
    context = {'questions':questions, 'category':category}
    return render(request,'fragenkatalog.html',context)

def categorylist(request):
    questions = Question.objects.all().order_by('date')
    categories = Category.objects.all().order_by('id')
    context = {'categories':categories, 'questions':questions}
    return render(request, 'categorylist.html', context)

def impressum(request):
    
    return render(request,'impressum.html')

def lobby_msg(request,pk):
    lobby = Lobby.objects.get(id=pk)
    p = None
    msg = 'None'
    q = None
    for part in lobby.participants.all():
        if part.user == request.user:
            p = part
    q = lobby.questions.all()[p.status]
    if request.method == 'POST':
        print(request.POST.get(q.question))
        if p.status <5:
            if q.answer_wrong_1 == request.POST.get(q.question):
                msg = q.answer_reason_1
            elif q.answer_wrong_2 == request.POST.get(q.question):
                msg = q.answer_reason_2
            elif q.answer_wrong_3 == request.POST.get(q.question):
                msg = q.answer_reason_3
            elif None == request.POST.get(q.question):
                msg = 'Keine Antwort!'
            else:
                msg = 'Richtig!'
    answers = [lobby.questions.all()[p.status].answer_correct,lobby.questions.all()[p.status].answer_wrong_1,lobby.questions.all()[p.status].answer_wrong_2,lobby.questions.all()[p.status].answer_wrong_3]
    random.shuffle(answers)
    context = {'lobby':lobby,'question':lobby.questions.all()[p.status],'answers':answers,'msg':msg,'ans':request.POST.get(q.question),'nr':p.status+1}
    return render(request,'lobby_msg.html',context)

def lobby(request,pk):
    lobby = Lobby.objects.get(id=pk)
    p = None
    msg = 'Keine Antwort!'
    for part in lobby.participants.all():
        if part.user == request.user:
            p = part
        else:
            print("Failed to get User!")
    if request.method == 'POST':
        q = lobby.questions.all()[p.status]
        if q.answer_correct ==  request.POST.get(q.question):
            p.score+=10
            p.correct+=1
        else:
            p.wrong+=1
        if p.status <4:
            p.status=p.status+1
            p.save()
            answers = [lobby.questions.all()[p.status].answer_correct,lobby.questions.all()[p.status].answer_wrong_1,lobby.questions.all()[p.status].answer_wrong_2,lobby.questions.all()[p.status].answer_wrong_3]
            random.shuffle(answers)
            context = {'lobby':lobby,'question':lobby.questions.all()[p.status],'answers':answers,'ans':request.POST.get(q.question), 'nr':p.status+1}
            return render(request,'lobby.html',context)

        else:
            p.status=p.status+1
            p.save()
            percent = p.score/(5*10) *100
            lobby.participants.remove(p)
            p.delete()
            participants = lobby.participants.all()
            lobby.save()
            if len(participants)==0:
                lobby.delete()
            context = {
                'score':p.score,
                'time': request.POST.get('timer'),
                'correct':p.correct,
                'wrong':p.wrong,
                'percent':percent,
                'total':5
            }
            return render(request,'result.html',context)

        
    else:
        context = {}
        participants = lobby.participants.all()
        if lobby.status==1:
            question = lobby.questions.all()[0]
            answers = [lobby.questions.all()[p.status].answer_correct,lobby.questions.all()[p.status].answer_wrong_1,lobby.questions.all()[p.status].answer_wrong_2,lobby.questions.all()[p.status].answer_wrong_3]
            random.shuffle(answers)
            context = {'lobby':lobby,'participants':participants,'question':question,'answers':answers}
        context = {'lobby':lobby,'participants':participants}
        return render(request,'lobby.html',context)

@login_required(login_url='login')
def create_lobby(request):
    print("wird ausgeführT")
    form = LobbyForm()
    if request.method == "POST":
        print(request.POST)
        #request.POST.get('name')....
        form = LobbyForm(request.POST)
        if form.is_valid():
            lobbyname = form.cleaned_data["name"]
            lobbymax_players = form.cleaned_data["max_players"]
            lobbycategory = form.cleaned_data["category"]
            lobby = Lobby(host=request.user,name=lobbyname,max_players=lobbymax_players,category=lobbycategory,status=0)
            lobby.save()
            participant = Participant(
                user = request.user,
                status =0,
                score = 0,
                wrong = 0,
                correct = 0,
                total = 0
                )
            participant.save()
            lobby.participants.add(participant)
            lobby.save()
            return redirect('lobby',pk=lobby.id)
            #return redirect('home')
        else:
            form = LobbyForm()

    context = {'form':form}
    return render(request,'question_form.html',context)

@login_required(login_url='login')
def join_lobby(request,pk):
    lobby = Lobby.objects.get(id=pk)
    participants = lobby.participants.all()
    if len(participants)<lobby.max_players:

        if len(Participant.objects.filter(user=request.user)):
            participant = Participant.objects.filter(user=request.user)[0]
        else:
            participant = Participant(
                user = request.user,
                status =0,
                score = 0,
                wrong = 0,
                correct = 0,
                total = 0
                )
            participant.save()
        lobby.participants.add(participant)
        participants = lobby.participants.all()
        lobby.save()
    else:
        print("Lobby full!")
    #context = {'lobby':lobby,'participants':participants,'question':question}
    return redirect('lobby',pk=lobby.id)
    #return render(request,'lobby.html',context)

def leave_lobby(request,pk):
    lobby = Lobby.objects.get(id=pk)
    participant = Participant.objects.filter(user=request.user)[0]
    lobby.participants.remove(participant)
    participant.delete()
    participants = lobby.participants.all()
    lobby.save()
    if len(participants)==0:
        lobby.delete()
        return redirect('home')
    #context = {'lobby':lobby,'participants':participants}
    return redirect('home')
    #return render(request,'lobby.html',context)

def start_lobby(request,pk):
    lobby = Lobby.objects.get(id=pk)
    p = None
    for part in lobby.participants.all():
        if part.user == request.user:
            p = part
    if lobby.status == 0:
        lobby.status = 1
        #achtung oder_by('?') wohl sehr langsam
        items = Question.objects.filter(category=lobby.category).order_by('?')[:5]
        for i in items:
            lobby.questions.add(i)
        lobby.save()
    answers = [lobby.questions.all()[0].answer_correct,lobby.questions.all()[0].answer_wrong_1,lobby.questions.all()[0].answer_wrong_2,lobby.questions.all()[0].answer_wrong_3]
    random.shuffle(answers)
    question = lobby.questions.all()[0]
    context ={'lobby':lobby,'question':question,'answers':answers,'nr':p.status+1}
    #return redirect('lobby',pk=lobby.id)
    return render(request,'lobby.html',context)

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
            messages.error(request,'Bei der registrierung ist ein Fehler aufgetreten')

    return render(request,'login_register.html',{'form':form})

def homepage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    form = LobbyForm()
    # if request.method == "POST":
    #     #print(request.POST)
    #     #request.POST.get('name')....
    #     form = LobbyForm(request.POST)
    #     if form.is_valid():
    #         lobbyname = form.cleaned_data["name"]
    #         lobbymax_players = form.cleaned_data["max_players"]
    #         lobbycategory = form.cleaned_data["category"]
    #         lobby = Lobby(host=request.user,name=lobbyname,max_players=lobbymax_players,category=lobbycategory,status=0)
    #         lobby.save()
    #         participant = Participant(
    #             user = request.user,
    #             status =0,
    #             score = 0,
    #             wrong = 0,
    #             correct = 0,
    #             total = 0
    #             )
    #         participant.save()
    #         lobby.participants.add(participant)
    #         lobby.save()
    #         return redirect('lobby',pk=lobby.id)
    #         #return redirect('home')
    #     else:
    #         form = LobbyForm()
    categories = Category.objects.all().order_by('id')
    LobbyList = Lobby.objects.all()
    context = {'categories':categories,'lobbylist':LobbyList, 'form':form}
    return render(request,'homepage.html', context)

def question_list(request):
    questions = Question.objects.all().order_by('date')
    return render(request, 'question_list.html', {'questions':questions})

@login_required(login_url='login')
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

@login_required(login_url='login')
def create_question(request):
    category = Category.objects.all().order_by('id')
    form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            questioncategory = form.cleaned_data['category']
            # cat = Category.objects.filter(name=f)[0]
            questionquestion = form.cleaned_data["question"]
            questionanswer_correct = form.cleaned_data["answer_correct"]
            questionanswer_wrong_1 = form.cleaned_data["answer_wrong_1"]
            questionanswer_wrong_2 = form.cleaned_data["answer_wrong_2"]
            questionanswer_wrong_3 = form.cleaned_data["answer_wrong_3"]
            questionanswer_reason_1 = form.cleaned_data["answer_reason_1"]
            questionanswer_reason_2 = form.cleaned_data["answer_reason_2"]
            questionanswer_reason_3 = form.cleaned_data["answer_reason_3"]
            question = Question(
                category=questioncategory, 
                question=questionquestion, 
                answer_correct=questionanswer_correct, 
                answer_wrong_1=questionanswer_wrong_1,
                answer_wrong_2=questionanswer_wrong_2, 
                answer_wrong_3=questionanswer_wrong_3,  
                answer_reason_1=questionanswer_reason_1,
                answer_reason_2=questionanswer_reason_2,
                answer_reason_3=questionanswer_reason_3 
                )
            question.save()
            return redirect('category_catalog',category_id=question.category.id)
            # return redirect('home')

    context = {'form':form, 'categories':category}
    return render(request,'question_form.html',context)

@login_required(login_url='login')
def create_question_defaultcategory(request, pk):
    form = QuestionFormDefaultCategory()
    if request.method == "POST":
        #print(request.POST)
        #request.POST.get('name')....
        form = QuestionFormDefaultCategory(request.POST)
        if form.is_valid():
            questioncategory = Category.objects.get(id=pk)
            #questionname = form.cleaned_data["name"]
            questionquestion = form.cleaned_data["question"]
            questionanswer_correct = form.cleaned_data["answer_correct"]
            questionanswer_wrong_1 = form.cleaned_data["answer_wrong_1"]
            questionanswer_wrong_2 = form.cleaned_data["answer_wrong_2"]
            questionanswer_wrong_3 = form.cleaned_data["answer_wrong_3"]
            questionanswer_reason_1 = form.cleaned_data["answer_reason_1"]
            questionanswer_reason_2 = form.cleaned_data["answer_reason_2"]
            questionanswer_reason_3 = form.cleaned_data["answer_reason_3"]
            question = Question(
                category=questioncategory, 
                #name=questionname, 
                question=questionquestion, 
                answer_correct=questionanswer_correct, 
                answer_wrong_1=questionanswer_wrong_1,
                answer_wrong_2=questionanswer_wrong_2, 
                answer_wrong_3=questionanswer_wrong_3,  
                answer_reason_1=questionanswer_reason_1,
                answer_reason_2=questionanswer_reason_2,
                answer_reason_3=questionanswer_reason_3 
                )
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



#AJAX

def llv(request):
    LobbyList = Lobby.objects.all()
    context = {'lobbylist':LobbyList}
    return render(request,'lobbylist.html', context)

def lobby_refresh(request,pk):
    lobby = Lobby.objects.get(id=pk)
    p  =None
    for part in lobby.participants.all():
        if part.user == request.user:
            p = part
    print("lobby refreshed!")
    #context = {"lobbyname":lobby.name,'lobbyid':lobby.id, "lobbystatus":lobby.status}
    context = {}
    if lobby.status:
        answers = [lobby.questions.all()[p.status].answer_correct,lobby.questions.all()[p.status].answer_wrong_1,lobby.questions.all()[p.status].answer_wrong_2,lobby.questions.all()[p.status].answer_wrong_3]
        random.shuffle(answers)
        context = {'lobby':lobby,'participants':lobby.participants.all(), 'question':lobby.questions.all()[p.status],'answers':answers}
    else:
        context = {'lobby':lobby,'participants':lobby.participants.all()}
    #return JsonResponse(context)
    return render(request,'lobbyinfo.html',context)

# def ajax_view(request,pk):
#     lobby = Lobby.objects.filter(id=pk).values()
#     obj = list(lobby.status)
#     return JsonResponse({'data':obj})

def is_ajax(request):
     return request.headers.get('x-requested-with') == 'XMLHttpRequest'

'''
# def index(request,id):
#     q = Question.objects.get(id=id)
#     print(request)
#     return render(request, 'one_question.html', {'question':q})

# def index2(request,id):
#     q = Question.objects.get(id=id)
#     return render(request, 'one_question.html', {'question':q})

# def room(request,pk):
#     room = Room.objects.get(id=pk)
#     room_messages = room.message_set.all().order_by('-date')
#     particitpants = room.participants.all()

#     if request.method == "POST":
#         message = Message.objects.create(
#             user=request.user,
#             room=room,
#             body=request.POST.get('body')
#         )
#         room.participants.add(request.user)
#         return redirect('room',pk=room.id)


#     context = {'room':room, 'room_messages':room_messages, 'particitpants':particitpants}
#     return render(request, 'room.html', context)

# @login_required(login_url='login')
# def create_room(request):
#     form = RoomForm()
#     if request.method == "POST":
#         form = RoomForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     context = {'form':form}
#     return render(request,'room_form.html',context)

# @login_required(login_url='login')
# def update_room(request,pk):
#     room = Room.objects.get(id=pk)
#     form = RoomForm(instance=room)
    
#     if request.user != room.host:
#         return HttpResponse('You are not allowed here!!')

#     if request.method == "POST":
#         form = RoomForm(request.POST, instance=room)
#         if form.is_valid():
#             form.save()
#             return redirect('home')

#     context = {'form':form}
#     return render(request,'room_form.html',context)

# @login_required(login_url='login')
# def delete_room(request,pk):
#     room = Room.objects.get(id=pk)
#     if request.method == "POST":
#         room.delete()
#         return redirect('home')
#     return render(request,"delete.html", {'obj':room})  

# @login_required(login_url='login')
# def delete_message(request,pk):
#     message = Message.objects.get(id=pk)

#     if request.user != message.user:
#         return HttpResponse('You are not allowed here!')

#     if request.method == "POST":
#         message.delete()
#         return redirect('home')
#     return render(request,"delete.html", {'obj':message})



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
    
    '''