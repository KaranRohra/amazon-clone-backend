from rest_framework import renderers

from django.shortcuts import HttpResponse
from django.http import JsonResponse

from . import models
from . import serializers

# Create your views here.

def index(request):
    user = models.User.objects.get(id=1)
    user_serialized = serializers.UserSerializer(user)
    print(user_serialized.data)

    users_seralized = serializers.UserSerializer(
        models.User.objects.all(),
        many=True
    )
    print(users_seralized.data)

    json_data = python_to_json(
        user_serialized.data
    )
    print(json_data)
    print()

    return JsonResponse({"user": user_serialized.data, "users": users_seralized.data})


def python_to_json(data):
    return renderers.JSONRenderer().render(data)
