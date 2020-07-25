from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def insert(request, user_id):
    return HttpResponse("Insert a record for user %s." % user_id)

def update(request, user_id):
    response = "Update a record for user %s."
    return HttpResponse(response % user_id)

def delete(request, user_id):
    return HttpResponse("Delete a record for user  %s." % user_id)