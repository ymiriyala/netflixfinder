from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect
from .models import userreg, userlog

# def showdetails(request):
#     cursor = connection.cursor()
#     # cursor.execute("call getUsers(@a)")
#     cursor.execute("call getUsers(@a)")
#     results = cursor.fetchall()
#     return render(request, 'Index.html', {'user': results})
#
# def addUser(request):
#     new_item = user(name = request.POST['name'])
#     cursor = connection.cursor()
#     cursor.callproc("addUser", [new_item.name])
#     return HttpResponseRedirect('/users/')

# def Register(request):
#     new_item = user(username = request.POST['username'], password = request.POST['password'], name = request.POST['name'])
#     cursor = connection.cursor()
#     cursor.callproc("addUser", [new_item.username, new_item.name, new_item.password])
#     return HttpResponseRedirect('/login/')

def Register(request):
    return render(request, 'register.html')

def NewRegistration(request):
    new_item = userreg(username = request.POST['username'], password = request.POST['password'], name = request.POST['name'])
    cursor = connection.cursor()
    cursor.callproc("addUser", [new_item.username, new_item.password, new_item.name])
    return HttpResponseRedirect('/login/')

def Login(request):
    return render(request, 'login.html')

def Home(request):
    new_item = userreg(username = request.POST['username'], password = request.POST['password'])
    cursor = connection.cursor()
    # args = [new_item.username, new_item.password, 0, 0]
    # cursor.callproc("getUser", args)
    # cursor.execute("""SELECT @_getUser_2, @_getUser_3""")
    cursor.execute("call getUser('" + new_item.username + "', '" + new_item.password + "', @p0, @p1)")
    results = cursor.fetchall()
    # results = results[0]
    userId = results[0][0]
    name = results[0][1]
    cursor = connection.cursor()
    cursor.execute("call getWatchedMovies(" + str(userId) + ", @p1)")
    results = cursor.fetchall()
    return render(request, 'home.html', {'results': results,'name': name})
# def AddMovie(request, pk):
