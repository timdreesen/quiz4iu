from django.contrib import admin
from .models import Question,Category,Room,Message,Topic,Lobby

# Register your models here.
admin.site.register(Question)
admin.site.register(Category)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Topic)
admin.site.register(Lobby)