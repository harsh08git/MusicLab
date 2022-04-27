
from pyexpat.errors import messages
from django.shortcuts import render, redirect
import pandas as pd
import random 
from django.http import HttpResponse
import json
import urllib.request
import re
from urllib3 import Retry
from django.contrib.auth.models import User 
from musicapp.models import Genres,Mood
from django.contrib import auth 
from django.contrib.auth.decorators import login_required
from django.contrib import messages


df2 = pd.read_csv('static/excel/spotify_songs.csv')
print(len(df2))
genre = Genres.objects.all()

if(len(genre) == 0):
    data = [
        Genres(
            track_name = df2['track_name'].values[i],
            artist_name = df2['track_artist'].values[i],
            genre = df2['playlist_genre'].values[i],
            popularity = df2['track_popularity'].values[i]
        )
        for i in range(len(df2))
    ]

    Genres.objects.bulk_create(data)
else:
    print('All Rows filled ', len(genre))


def landing(request):
    return render(request,'landing.html')

def youtube_link(search_keyword):
    search_keyword = search_keyword.replace(' ' ,'_')
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return "https://www.youtube.com/watch?v=" + video_ids[0]

def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')

        if User.objects.filter(username = username).first():
            messages.error(request, "This username is already taken")
            return redirect('/register')


        if len(username)<10:
            messages.error(request, " Your user name must be greater 10 characters")
            return redirect('/register')

        if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('/register')
        
        SpecialSym =['$', '@', '#', '%']
        
        if len(password) < 8:
            messages.error(request,'length should be at least 6')
            return redirect('/register')

            
        if not any(char.isdigit() for char in password):
            messages.error(request,'Password should have at least one numeral')
            return redirect('/register')


            
        if not any(char.isupper() for char in password):
            messages.error(request,'Password should have at least one uppercase letter')
            return redirect('/register')


            
        if not any(char.islower() for char in password):
            messages.error(request,'Password should have at least one lowercase letter')
            return redirect('/register')


            
        if not any(char in SpecialSym for char in password):
            messages.error(request,'Password should have at least one of the symbols $@#')
            return redirect('/register')


        
        user=User.objects.create_user(username=username,password=password,email=email)
        user.save()
        messages.success(request, " Your MLAB account has been successfully created")
        return redirect('/login')
    else:
        return render(request,'register.html')




def login(request):
    if request.method=='POST':
        password=request.POST.get('password')
        username=request.POST.get('username')
        user=auth.authenticate(username= username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'Successfully Logged in ')
            # print(user.is_active)
            #auth.login(request,userObj)
            return redirect('/account')
        
        else:
            messages.error(request,'Invalid Credentials')         
            return redirect('/login')
    
    return render(request,'login.html')

def logoutuser(request):
    auth.logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')

@login_required(login_url='login')
def index(request):  
    df = pd.read_csv('static/excel/final_songs.csv')
    print(len(df))
    mood = Mood.objects.all()

    if(len(mood) == 0):
        data = [
            Mood(
                track_name = df['track_name'].values[i],
                artist_name = df['track_artist'].values[i],
                mood = df['mood'].values[i]
            )
            for i in range(len(df))
        ]
        Mood.objects.bulk_create(data)
    else:
        print('All Rows filled ', len(mood))
    
    return render(request,'index.html')


def response(request):
    
    if (request.method == 'POST'):
        message = request.POST.get('the_post')
        response_data = {}
        response_data['message'] = message

        song_dict = {}
        if ('sad' in message):  
            moods = Mood.objects.all().filter(mood= "Sad")
            songs = []
            for i in moods:
                songs.append(i.artist_name + '_' + i.track_name )
            random.shuffle(songs) 
            for i in range(15):
                try:
                    song_dict[i] = {
                        'name' : songs[i].split('_')[1],
                        'link' : youtube_link(songs[i]),
                    }
                except Exception as e:
                    print(songs[i])
                pass
            song_dict['response'] = 'Listen to these songs and remember you are best' 
            print(song_dict)
        
        elif ('calm' in message):
            moods = Mood.objects.all().filter(mood= "Calm")
            songs = []
            for i in moods:
                songs.append(i.artist_name + '_' + i.track_name )
            random.shuffle(songs) 
            for i in range(15):
                try:
                    song_dict[i] = {
                        'name' : songs[i].split('_')[1],
                        'link' : youtube_link(songs[i]),
                    }
                except Exception as e:
                    print(songs[i])
                pass
            song_dict['response'] = 'Listen to these songs and have a peaceful listening experience' 
            print(song_dict)

        elif ('energetic' in message):
            moods = Mood.objects.all().filter(mood= "Energetic")
            songs = []
            for i in moods:
                songs.append(i.artist_name + '_' + i.track_name )
            random.shuffle(songs) 
            for i in range(15):
                try:
                    song_dict[i] = {
                        'name' : songs[i].split('_')[1],
                        'link' : youtube_link(songs[i]),
                    }
                except Exception as e:
                    print(songs[i])
                pass
            song_dict['response'] = 'Listen to these songs and dance your heart out' 
            print(song_dict)

        elif ('happy' in message):
            moods = Mood.objects.all().filter(mood= "Happy")
            songs = []
            for i in moods:
                songs.append(i.artist_name + '_' + i.track_name )
            random.shuffle(songs) 
            for i in range(15):
                try:
                    song_dict[i] = {
                        'name' : songs[i].split('_')[1],
                        'link' : youtube_link(songs[i]),
                    }
                except Exception as e:
                    print(songs[i])
                pass
            song_dict['response'] = 'Listen to these songs and spread happiness to others' 
            print(song_dict)

        return HttpResponse(
            json.dumps(song_dict),
            content_type="application/json",
                        
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )




def genre(request,given_genre):
    if(given_genre == 'pop'):
        song_dict = {}
        genre = Genres.objects.all().filter(genre= given_genre)
        songs = []
        for i in genre:
            songs.append(i.artist_name + '_' + i.track_name )
    
        random.shuffle(songs)
        
        for i in range(10):
            try:
                song_dict[i] = {
                    'name' : songs[i].split('_')[1],
                    'link' : youtube_link(songs[i]),
                    'artist' : songs[i].split('_')[0]
                }
            except Exception as e:
                print(songs[i])
                pass
        
        song_dict = {'dict' : song_dict}
        print(song_dict)
        song_dict['genre'] = given_genre

        return render(request,'genre.html',song_dict)

    
    elif(given_genre == 'rap'):
        song_dict = {}
        genre = Genres.objects.all().filter(genre= given_genre )
        songs = []
        for i in genre:
            songs.append(i.artist_name + '_' + i.track_name )
    
        random.shuffle(songs)
        
        for i in range(10):
            try:
                song_dict[i] = {
                    'name' : songs[i].split('_')[1],
                    'link' : youtube_link(songs[i]),
                    'artist' : songs[i].split('_')[0]
                }
            except Exception as e:
                print(songs[i])
                pass
        
        song_dict = {'dict' : song_dict}
        print(song_dict)
        song_dict['genre'] = given_genre

        return render(request,'genre.html',song_dict)
    
    elif(given_genre == 'rock'):
        song_dict = {}
        genre = Genres.objects.all().filter(genre= given_genre )
        songs = []
        for i in genre:
            songs.append(i.artist_name + '_' + i.track_name )
    
        random.shuffle(songs)
        
        for i in range(10):
            try:
                song_dict[i] = {
                    'name' : songs[i].split('_')[1],
                    'link' : youtube_link(songs[i]),
                    'artist' : songs[i].split('_')[0]
                }
            except Exception as e:
                print(songs[i])
                pass
        
        song_dict = {'dict' : song_dict}
        print(song_dict)
        song_dict['genre'] = given_genre

        return render(request,'genre.html',song_dict)

    elif(given_genre == 'latin'):
        song_dict = {}
        genre = Genres.objects.all().filter(genre= given_genre )
        songs = []
        for i in genre:
            songs.append(i.artist_name + '_' + i.track_name )
    
        random.shuffle(songs)
        
        for i in range(10):
            try:
                song_dict[i] = {
                    'name' : songs[i].split('_')[1],
                    'link' : youtube_link(songs[i]),
                    'artist' : songs[i].split('_')[0]
                }
            except Exception as e:
                print(songs[i])
                pass
        
        song_dict = {'dict' : song_dict}
        print(song_dict)
        song_dict['genre'] = given_genre
        return render(request,'genre.html',song_dict)

    elif(given_genre == 'rnb'):
        song_dict = {}
        genre = Genres.objects.all().filter(genre= given_genre )
        songs = []
        for i in genre:
            songs.append(i.artist_name + '_' + i.track_name )
    
        random.shuffle(songs)
        
        for i in range(10):
            try:
                song_dict[i] = {
                    'name' : songs[i].split('_')[1],
                    'link' : youtube_link(songs[i]),
                    'artist' : songs[i].split('_')[0]
                }
            except Exception as e:
                print(songs[i])
                pass
        
        song_dict = {'dict' : song_dict}
        print(song_dict)
        song_dict['genre'] = given_genre
        return render(request,'genre.html',song_dict)

    elif(given_genre == 'edm'):
        song_dict = {}
        genre = Genres.objects.all().filter(genre= given_genre )
        songs = []
        for i in genre:
            songs.append(i.artist_name + '_' + i.track_name )
    
        random.shuffle(songs)
        
        for i in range(10):
            try:
                song_dict[i] = {
                    'name' : songs[i].split('_')[1],
                    'link' : youtube_link(songs[i]),
                    'artist' : songs[i].split('_')[0]
                }
            except Exception as e:
                print(songs[i])
                pass
        
        song_dict = {'dict' : song_dict}
        song_dict['genre'] = given_genre
        print(song_dict)

        return render(request,'genre.html',song_dict)

    elif(given_genre == 'top30'):
        song_dict = {}
        genre = Genres.objects.all().order_by('-popularity')
        songs = []
        artistList = []
        for i in genre:
            if(i.track_name not in songs):
                songs.append(i.track_name )
                artistList.append(i.artist_name + '_' + i.track_name )
            else:
                pass
    
        
        for i in range(30):
            try:
                song_dict[i] = {
                    'name' : artistList[i].split('_')[1],
                    'link' : youtube_link(artistList[i]),
                    'artist' : artistList[i].split('_')[0]
                }
            except Exception as e:
                print(artistList[i])
                pass
        
        song_dict = {'dict' : song_dict}
        song_dict['genre'] = given_genre
        print(song_dict)

        return render(request,'genre.html',song_dict)

        


def fetch(request,song):
    genre = Genres.objects.filter(track_name__startswith = song)
    
    if(len(genre) != 0):
        genre = genre[0]
        results = {
            'name' : genre.track_name,
            'artist' : genre.artist_name,
            'link' : youtube_link(genre.artist_name + '_' + genre.track_name),

        }

        results = {'dict' : results}
        # print(results)


        return render(request,'landing.html' , results)

    else:
        results = {'dict' : None}
        return render(request,'landing.html',results)

    




        
            


        
    