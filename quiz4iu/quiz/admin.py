from django.contrib import admin
from .models import Question,Category,Lobby,Participant #,Room,Message,Topic

# Register your models here.
admin.site.register(Question)
admin.site.register(Category)
admin.site.register(Lobby)
admin.site.register(Participant)
# admin.site.register(Room)
# admin.site.register(Message)
# admin.site.register(Topic)