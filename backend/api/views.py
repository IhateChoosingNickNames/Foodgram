from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response


def smth(request):
    return Response({"bla": request.method})