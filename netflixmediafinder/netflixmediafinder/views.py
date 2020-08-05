from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect
from .models import userreg, userlog, insertMovie, removeMovie, searchMovie, editRating
import numpy as np
import operator
import requests
import time

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
    cursor.close()

    cursor = connection.cursor()
    cursor.execute("call highestRatedMovies(@p0, @p1, @p2)")
    results2 = cursor.fetchall()
    print(len(results2))
    cursor.close()

    cursor = connection.cursor()
    cursor.execute("call popularMovies(@p0, @p1, @p2)")
    results3 = cursor.fetchall()
    cursor.close()

    return render(request, 'login.html', {'results': results, 'results2': results2, 'results3':results3})


def UserProfile(request):
    new_item = userreg(username = request.POST['username'], password = request.POST['password'])
    cursor = connection.cursor()
    cursor.execute("call getUser('" + new_item.username + "', '" + new_item.password + "', @p0, @p1, @p2, @p3, @p4, @p5, @p6)")
    results = cursor.fetchall()
    userId = results[0][0]
    name = results[0][1]
    a = results[0][2]
    c = results[0][3]
    e = results[0][4]
    n = results[0][5]
    o = results[0][6]
    context = {'username': new_item.username, 'password': new_item.password, 'agreeableness': a, 'conscientiousness': c, 
    'extraversion': e, 'neuroticism': n, 'openness': o}
    return render(request, 'userprofile.html', context)

def SearchMovie(request):
    new_item = searchMovie(name = request.POST['name'])
    cursor = connection.cursor()
    cursor.execute("call searchIMDbTitles('" + new_item.name + "', @p1, @p2, @p3, @p4, @p5, @p6, @p7, @p8)")
    results = cursor.fetchall()
    return render(request, 'searchmovie.html', {'results': results})


def AddMovie(request):
    new_item = insertMovie(password = request.POST['password'], username = request.POST['username'], name = request.POST['name'], rating = request.POST['rating'], userId = request.POST['userId'])
    cursor = connection.cursor()
    name = new_item.name
    index = name.find("'")
    if index != -1:
        name = name[:index] + "'" + name[index:]
    print(name)
    cursor.execute("call getTitleId('" + name + "', @p1)")
    results = cursor.fetchall()
    if not results:
        return render(request, 'addmovie.html', {'username': new_item.username, 'password': new_item.password, 'error': 1})
    else:
        titleId = results[0][0]
        cursor = connection.cursor()
        cursor.callproc("addWatchInstance", [new_item.userId, titleId, new_item.rating])
        return render(request, 'addmovie.html', {'username': new_item.username, 'password': new_item.password, 'error': 0})


def RemoveMovie(request):
    new_item = removeMovie(password = request.POST['password'], username = request.POST['username'], userId = request.POST['userId'], titleId = request.POST['titleId'], watchId = request.POST['watchId'])
    cursor = connection.cursor()
    cursor.callproc("deleteWatchInstance", [new_item.watchId])
    return render(request, 'removemovie.html', {'username': new_item.username, 'password': new_item.password})


def EditRating(request):
    new_item = editRating(password = request.POST['password'], username = request.POST['username'], userId = request.POST['userId'], titleId = request.POST['titleId'], rating = request.POST['rating'])
    cursor = connection.cursor()
    cursor.callproc("updateRating", [new_item.userId, new_item.titleId, new_item.rating])
    return render(request, 'editrating.html', {'username': new_item.username, 'password': new_item.password})


def Watchlist(request):
    new_item = userreg(username = request.POST['username'], password = request.POST['password'])
    cursor = connection.cursor()
    # args = [new_item.username, new_item.password, 0, 0]
    # cursor.callproc("getUser", args)
    # cursor.execute("""SELECT @_getUser_2, @_getUser_3""")
    cursor.execute("call getUser('" + new_item.username + "', '" + new_item.password + "', @p0, @p1, @p2, @p3, @p4, @p5, @p6)")
    results = cursor.fetchall()
    cursor.close()
    # results = results[0]
    userId = results[0][0]
    name = results[0][1]
    cursor = connection.cursor()
    cursor.execute("call getWatchedMovies(" + str(userId) + ", @p0, @p1, @p2, @p3)")
    results = cursor.fetchall()
    print(results)
    return render(request, 'watchlist.html', {'results': results,'name': name, 'userId': userId, 'username': new_item.username, 'password': new_item.password})

def Recommendations(request):
    new_item = userreg(username = request.POST['username'], password = request.POST['password'])
    cursor = connection.cursor()
    cursor.execute("call getUser('" + new_item.username + "', '" + new_item.password + "', @p0, @p1, @p2, @p3, @p4, @p5, @p6)")
    results = cursor.fetchall()
    cursor.close()
    userId = int(results[0][0])

    cursor = connection.cursor()
    cursor.execute('call getNetflixTitles(@p0, @p1, @p2, @p3)')
    netflix_titles = cursor.fetchall()
    cursor.close()

    cursor = connection.cursor()
    cursor.execute('call getUserItemData(@p0, @p1, @p2, @p3, @p4, @p5, @p6, @p7, @p8)')
    userItemData = cursor.fetchall()
    cursor.close()
    for result in userItemData:
        print(result)

    cursor = connection.cursor()
    cursor.execute('call getRaters("tt0314353")')
    results = cursor.fetchall()
    for result in results:
        print(result)
    cursor.close()

    def personalitySimilarityScore(userid_a, userid_b):
        cursor = connection.cursor()
        cursor.execute("call getUserPersonality(" + str(userid_a) + ")")
        a_personality = cursor.fetchall()[0]
        cursor.close()

        cursor = connection.cursor()
        cursor.execute("call getUserPersonality(" + str(userid_b) + ")")
        b_personality = cursor.fetchall()[0]
        cursor.close()

        distance = 0
        for i in range(5):
            distance += (a_personality[i] - b_personality[i])*(a_personality[i] - b_personality[i])
        return 1 - distance/125

    def getNewYorkTimesReview(title):
        api_key = 'ATn6xl3sE1MbaOeskyFC28ZgmKvCuxoQ'
        api_route = 'https://api.nytimes.com/svc/movies/v2/reviews/search.json?query=%s&api-key=%s' % (title, api_key)
        response = requests.get(api_route)
        data = response.json()
        print(data)
        if not ('num_results' in data):
            return 0
        num_results = data['num_results']
        if num_results == 0:
            return num_results
        for result in data["results"]:
            if title == result["display_title"]:
                url = result["link"]["url"]
                return url


    print(personalitySimilarityScore(userId, userId))
    score_vector = []

    cursor = connection.cursor()
    cursor.execute("call getWatchedMovies("  + str(userId) + ", @p0, @p1, @p2, @p3)")
    movieItems = cursor.fetchall()
    cursor.close()

    seenMovies = {i[0]:1 for i in movieItems}


    for title in netflix_titles:
        #calculate based on watch list
        titleId = title[0]
        if titleId in seenMovies:
            continue

        cursor = connection.cursor()
        cursor.execute("call getRaters('" + str(title[0])+ "')")
        rater_info = cursor.fetchall()
        cursor.close()

        score = 0
        personality_similarity_sum = 0
        for i in range(len(rater_info)):
            peer_id = rater_info[i][0]
            peer_rating = rater_info[i][1]

            personality_similarity = personalitySimilarityScore(userId, peer_id)
            score += personality_similarity * peer_rating
            personality_similarity_sum += personality_similarity

        score /= personality_similarity_sum + .001
        #imdb stuff: weighted n%
        rating = title[1]
        votes = title[2]
        if not rater_info:
            score = rating
            if votes < 30000:
                score *= votes / 30000.0
        else:
            score = (0.75)*score + (0.25)*rating

        score_vector.append((score, titleId))
  
    #finish
    score_vector.sort(key = operator.itemgetter(0))
    recommendations = []
    for score_tuple in score_vector[-15:-1]:
        titleId = score_tuple[1]
        cursor = connection.cursor()
        cursor.execute("call getShowId('" + str(titleId) + "')")
        showid = int(cursor.fetchall()[0][0])
        cursor.close()
        predictedScore = score_tuple[0]

        cursor = connection.cursor()
        cursor.execute("call getRecommendationInfo(" + str(showid) + ")")
        results = cursor.fetchall()
        cursor.close()
        titleName = results[0][0]
        releaseYear = results[0][1]
        parental = results[0][2]
        duration = results[0][3]
        listedIn = results[0][4]
        description = results[0][5]
        director = results[0][6]
        url = getNewYorkTimesReview(titleName)

        recommendations.append((titleName, showid, releaseYear, parental, duration, listedIn, description, director, url))

    print(recommendations)
    return render(request, 'recommendations.html', {'userId': userId, 'username':new_item.username, 'password': new_item.password, 'recommendations': recommendations})


def Agreeableness(request):
    new_item = userreg(username = request.POST['username'], password = request.POST['password'])
    context = {'username': new_item.username, 'password': new_item.password}
    return render(request, 'test_agreeableness.html', context)


def Conscientiousness(request):
    new_item = userreg(username = request.POST['username'], password = request.POST['password'])
    context = {'username': new_item.username, 'password': new_item.password}
    return render(request, 'test_conscientiousness.html', context)


def Extraversion(request):
    new_item = userreg(username = request.POST['username'], password = request.POST['password'])
    context = {'username': new_item.username, 'password': new_item.password}
    return render(request, 'test_extraversion.html', context)


def Neuroticism(request):
    new_item = userreg(username = request.POST['username'], password = request.POST['password'])
    context = {'username': new_item.username, 'password': new_item.password}
    return render(request, 'test_neuroticism.html', context)


def Openness(request):
    new_item = userreg(username = request.POST['username'], password = request.POST['password'])
    context = {'username': new_item.username, 'password': new_item.password}
    return render(request, 'test_openness.html', context)


def UpdateAttribute(request):
    new_item = userreg(username = request.POST['username'], password = request.POST['password'])
    attribute = request.POST['attribute']
    cursor2 = connection.cursor()
    cursor2.execute("call getUser('" + new_item.username + "', '" + new_item.password + "', @p0, @p1, @p2, @p3, @p4, @p5, @p6)")
    results = cursor2.fetchall()
    UserId = results[0][0]
    q1 = int(request.POST['q1'])
    q2 = int(request.POST['q2'])
    q3 = int(request.POST['q3'])
    q4 = int(request.POST['q4'])
    q5 = int(request.POST['q5'])
    q6 = int(request.POST['q6'])
    q7 = int(request.POST['q7'])
    q8 = int(request.POST['q8'])
    q9 = int(request.POST['q9'])
    q10 = int(request.POST['q10'])
    computedScore = round(sum([q1, q2, q3, q4, q5, q6, q7, q8, q9, q10])/10)
    cursor = connection.cursor()
    if attribute == 'agreeableness':
        cursor.callproc('updateUserAgreeableness', [computedScore, UserId])
    elif attribute == 'conscientiousness':
        cursor.callproc('updateUserConscientiousness', [computedScore, UserId])
    elif attribute == 'extraversion':
        cursor.callproc('updateUserExtraversion', [computedScore, UserId])
    elif attribute == 'neuroticism':
        cursor.callproc('updateUserNeuroticism', [computedScore, UserId])
    elif attribute == 'openness':
        cursor.callproc('updateUserOpenness', [computedScore, UserId])
    context = {'username': new_item.username, 'password': new_item.password, 'attribute': attribute, 'computedScore': computedScore}
    return render(request, 'updateattribute.html', context)


def Details(request, show_id):
    def getNewYorkTimesReview(title):
        api_key = 'ATn6xl3sE1MbaOeskyFC28ZgmKvCuxoQ'
        api_route = 'https://api.nytimes.com/svc/movies/v2/reviews/search.json?query=%s&api-key=%s' % (title, api_key)
        response = requests.get(api_route)
        data = response.json()
        print(data)
        if not ('num_results' in data):
            return 0
        num_results = data['num_results']
        if num_results == 0:
            return num_results
        for result in data["results"]:
            if title == result["display_title"]:
                url = result["link"]["url"]
                return url
        return 0

    def getTmdbPoster(title):
        api_key = '833155305c00d9a696861d9c9c864659'
        api_route = 'https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s&page=1&include_adult=false' % (api_key, title)
        response = requests.get(api_route)
        data = response.json()
        print(data)
        total_results = data['total_results']
        if total_results == 0:
            return 0
        for result in data['results']:
            if title == result["title"]:
                poster_path = result["poster_path"]
                return poster_path
        return 0

    cursor = connection.cursor()
    cursor.execute("call getRecommendationInfo(" + str(show_id) + ")")
    results = cursor.fetchall()
    title = results[0][0]
    releaseYear = results[0][1]
    parental = results[0][2]
    duration = results[0][3]
    listedIn = results[0][4]
    description = results[0][5]
    director = results[0][6]
    cursor.close()

    cursor = connection.cursor()
    cursor.execute("call getImdbRating(" + str(show_id) + ")")
    results2 = cursor.fetchall()
    imdb_rating = results2[0][0]
    cursor.close()

    review_url = getNewYorkTimesReview(title)
    poster_path = 'http://image.tmdb.org/t/p/w342/' + getTmdbPoster(title)
    context = {'title': title, 'releaseYear':releaseYear, 'parental': parental, 'duration':duration, 'genres':listedIn, 
    'description':description, 'director':director, 'imdb_rating':imdb_rating, 'review_url':review_url, 'poster_path':poster_path}

    return render(request, 'details.html', context)