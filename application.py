import requests 
import base64
import datetime
from urllib.parse import urlencode
import json

#information to fill out
user_id = "3hoqlfah25ej3gr7e4x3vsf4c"
client_id = "f2ace4e1b01a4385af648c12a8b0879e"
secret_client = "1d0aa652e0e34680a4c13ee7d033402f"
spotify_token = "BQAciqmdhVQVsdivL-J4cFt8gb5HFSutv0GzsPfEAxse9NUyrgYIT7hr00DF-Cfwe3olqRAJH_Ypl2fhOAWfetEUI09hd30zAJcjN4Gyn5PX6ZYcT32v6HorEdCEvvoyfDCovKRsyn8vklG54xJLvOUMOz6RNYcM7YTpTfe-fdiCHkFjQDQKstInYPUbFjf-r40maOkqzMrzntMQJgdOAu6r6bNoEtMf"

class YouTubeMusic(object):
    user_id = None
    client_id = None
    secret_client = None
    spotify_token = None
    
    def __init__(self,user_id,client_id,secret_client,spotify_token):
        '''
        initializes user_id, client_id, secret_client, spotify_token
        '''
        self.user_id = user_id
        self.client_id = client_id
        self.secret_client = secret_client
        self.spotify_token = spotify_token
    
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
        header = headers = {"Authorization":f"Bearer {self.spotify_token}"}

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
                print(r.json(),title, "added to playlist")
    
    def multiadd(self,titles, playlist_id):
        for title in titles:
            self.addsong(title,playlist_id)



client = YouTubeMusic(user_id,client_id,secret_client,spotify_token)
temp = client.newplaylist(name = "single dogs")
client.multiadd(["WAP","S14/7/365","Adore You"], temp)