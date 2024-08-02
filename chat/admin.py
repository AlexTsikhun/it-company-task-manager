from django.contrib import admin


from chat.models import ChatMessage, Thread

admin.site.register(ChatMessage)

admin.site.register(Thread)
