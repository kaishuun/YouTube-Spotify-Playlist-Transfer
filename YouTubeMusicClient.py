import requests 
import base64
import datetime
from urllib.parse import urlencode
import json

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import googleapiclient.errors

class YouTubeMusic(object):
    user_id = None
    client_id = None
    secret_client = None
    spotify_token = None
    youtube_key = None
    
    def __init__(self,user_id,spotify_token, youtube_key):
        '''
        initializes user_id, client_id, secret_client, spotify_token, youtube_key
        '''
        self.user_id = user_id
        self.spotify_token = spotify_token
        self.youtube_key = youtube_key
    
    def newplaylist(self, name = "new playlist", public = True, collaborative = False):
        #creates a new empty spotify playlist
        endpoint = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        header = {
                    "Authorization":f"Bearer {self.spotify_token}",
                    "Content-Type":"application/json"
                }
        r = requests.post(endpoint,data = json.dumps({"name":name, "public":public,"collaborative":collaborative}), headers = header)
       
        #returns a playlist if successful, if not it prints a failure message
        if r.status_code in range(200,299):
            return(r.json()["id"])
            print("playlist:",name, "created")
        else:
            print("playlist not created")
        
    def search(self,title, spec):
        endpoint = "https://api.spotify.com/v1/search"
        header = {"Authorization":f"Bearer {self.spotify_token}"}

        data = urlencode({"q":title,
               "type":spec.lower(),
                "limit":1})

        lookup_url = f"{endpoint}?{data}"
        #queries for a title and return {} if not found, else returns the json 
        r = requests.get(lookup_url, headers = header)
        if r.status_code in range(200,299):
            return r.json()
        else:
            print(title, "not found")
            return {}


    def search_get_uri(self,title,spec):
        #gets the uri from the search, if not successful returns {}
        result =  self.search(title,spec)
        try:
            return result["tracks"]["items"][0]["uri"]
        except:
            return '';
    
    def addsong(self,title,playlist_id):
        #gets the uris from each and if the uri is not found it is skipped
        if playlist_id == None:
            raise Exception("No playlist is selected")
            
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        header = {
                    "Authorization":f"Bearer {self.spotify_token}",
                    "Content-Type":"application/json"
                }
        
        track_uri = self.search_get_uri(title,"track")
        if not track_uri:
            print(title,"not added to playlist")
            return
        else:
            data = urlencode({"uris":track_uri})
        
            #final checks to check song validity
            lookup_url = f"{endpoint}?{data}"
            r = requests.post(lookup_url,headers = header)
            if r.status_code not in range(200,299):
                print(title, "not added to playlist")
            else:
                print(title, "added to playlist")
    
    def multiadd(self,titles, playlist_id):
        for title in titles:
            self.addsong(title,playlist_id)
            
    def getyoutubeplaylist(self, playlistId):
        #sets up and deploys the request
        try:
            youtube = build('youtube','v3',developerKey = self.youtube_key)
            request = youtube.playlistItems().list(
                    part="snippet",
                    maxResults=50,
                    playlistId=playlistId
                )
        except:
            raise Exception("Playlist Invalid")
            
        r = request.execute()

        #appends the dict to a list of songs
        results = []
        for i in r['items']:
            results.append(i['snippet']['title'])
        return results

    def playlisttransfer(self, youtube_playlistId, spotify_playlisttitle, public = True, collaborative = False):
        #gets the songs and creates a new playlist
        songs = self.getyoutubeplaylist(youtube_playlistId)
        spotify_playlistId = self.newplaylist(spotify_playlisttitle, public, collaborative)
        self.multiadd(songs, spotify_playlistId)