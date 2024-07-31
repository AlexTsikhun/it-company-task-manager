from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Message


def room_view(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    messages = room.messages.all()
    return render(request, "chat/room.html", {"room": room, "messages": messages})


def send_message(request, room_name):
    if request.method == "POST":
        room = get_object_or_404(Room, name=room_name)
        message_content = request.POST.get("message", None)
        if message_content:
            Message.objects.create(
                room=room, sender=request.user, content=message_content
            )
    return redirect("room_view", room_name=room_name)
