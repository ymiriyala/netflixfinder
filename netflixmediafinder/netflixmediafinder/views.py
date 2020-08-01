from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect
from .models import userreg, userlog, insertMovie, removeMovie, searchMovie, editRating

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
    cursor = connection.cursor()
    cursor.execute("call getTopTen(@p0, @p1, @p2)")
    results = cursor.fetchall()
    return render(request, 'login.html', {'results': results})

def SearchMovie(request):
    new_item = searchMovie(name = request.POST['name'])
    cursor = connection.cursor()
    cursor.execute("call searchIMDbTitles('" + new_item.name + "', @p1, @p2, @p3, @p4, @p5, @p6, @p7, @p8)")
    results = cursor.fetchall()
    return render(request, 'searchmovie.html', {'results': results})

def AddMovie(request):
    new_item = insertMovie(password = request.POST['password'], username = request.POST['username'], name = request.POST['name'], rating = request.POST['rating'], userId = request.POST['userId'])
    cursor = connection.cursor()
    cursor.execute("call getTitleId('" + new_item.name + "', @p1)")
    results = cursor.fetchall()
    titleId = results[0][0]
    cursor = connection.cursor()
    cursor.callproc("addWatchInstance", [new_item.userId, titleId, new_item.rating])
    return render(request, 'addmovie.html', {'username': new_item.username, 'password': new_item.password})

def RemoveMovie(request):
    new_item = removeMovie(password = request.POST['password'], username = request.POST['username'], userId = request.POST['userId'], titleId = request.POST['titleId'])
    cursor = connection.cursor()
    cursor.callproc("deleteWatchInstance", [new_item.userId, new_item.titleId])
    return render(request, 'removemovie.html', {'username': new_item.username, 'password': new_item.password})

def EditRating(request):
    new_item = editRating(password = request.POST['password'], username = request.POST['username'], userId = request.POST['userId'], titleId = request.POST['titleId'], rating = request.POST['rating'])
    cursor = connection.cursor()
    cursor.callproc("updateRating", [new_item.userId, new_item.titleId, new_item.rating])
    return render(request, 'editrating.html', {'username': new_item.username, 'password': new_item.password})

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
    cursor.execute("call getWatchedMovies(" + str(userId) + ", @p1, @p2)")
    results = cursor.fetchall()
    return render(request, 'home.html', {'results': results,'name': name, 'userId': userId, 'username': new_item.username, 'password': new_item.password})
