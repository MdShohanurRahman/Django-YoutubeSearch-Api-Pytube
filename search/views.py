import requests
import time
from isodate import parse_duration

from django.conf import settings
from django.shortcuts import render, redirect
from pytube import YouTube
from pytube import Playlist
import os.path
from django.contrib import messages

def index(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part' : 'snippet',
            'q' : request.POST['search'],
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 9,
            'type' : 'video'
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 9
        }

        r = requests.get(video_url, params=video_params)

        results = r.json()['items']

        
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_data)

    context = {
        'videos' : videos
    }
    
    return render(request, 'search/index.html', context)



def download_video(request):
    homedir = os.path.expanduser("~")
    dirs=homedir +'/Downloads/pytube'

    if request.method == "POST":
        url=request.POST.get('link')

        if os.path.exists(dirs) == False:
        	os.mkdir(dirs)
        
        YouTube(url).streams.first().download(dirs)
        messages.success(request, f'Download completed. Check your "{dirs}" directory!')
    return render(request, 'pytube/download_video.html')


def download_audio(request):
    homedir = os.path.expanduser("~")
    dirs=homedir +'/Downloads/pytube'
    download = False # click to show directory boolien type

    if request.method == "POST":
        url=request.POST.get('link')

        if os.path.exists(dirs) == False:
        	os.mkdir(dirs)

        filename = YouTube(url).title
        
        if os.path.exists(dirs+'/'+filename) == False:
        	YouTube(url).streams.filter(only_audio=True).first().download(dirs)
        	messages.success(request, f'download completed. Check your "{dirs}" directory!')
        	download = True


        
        else:
        	messages.success(request, f'{filename} already exists. Check your"{dirs}" directory!')
        	download = True

    return render(request, 'pytube/download_audio.html',{
    	'download' : download,
    	})
  

def download_playlist(request):
    homedir = os.path.expanduser("~")
    dirs=homedir +'/Downloads/pytube/playlists'

    if request.method == "POST":
        url=request.POST.get('link')
        filename = url.split('=')[1][1:5]
        dirs = dirs+'/'+filename
        if os.path.exists(dirs) == False:
        	os.mkdir(dirs)
      
        pl = Playlist(url)
        pl.download_all(dirs)
        messages.success(request, f'Download completed. Check your "{dirs}" directory!')
    return render(request, 'pytube/download_playlists.html')