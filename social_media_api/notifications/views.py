from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from .models import Notification

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def notification_list(request):

    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by("-timestamp")

    data = [
        {
            "actor": n.actor.username,
            "verb": n.verb,
            "time": n.timestamp,
            "read": n.is_read,
        }
        for n in notifications
    ]

    return Response(data)

