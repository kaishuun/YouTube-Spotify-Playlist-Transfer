# YouTube-Playlist-to-Spotify-Playlist

## Introduction

This program converts YouTube playlists containing music or podcasts to Spotify playlists by using the YouTube Data API and Spotify Web API.

It has allowed me to explore more about data extraction, filtering, and generally working with the requests library and working with json formatting in python. I have successfully implemented an API client that is able to search for music on Spotify, create playlists, as well as add lists of songs onto said playlists.

## Using the Application
To use the python program, you would need information from both of the YouTube and Spotify applications, specifically:

Spotify:

- User Id (this could be found by going to your profile and copying your username)
- Spotify Token (this is the authorization token that allows the API to create and update playlists, that could be found by running a test example from the sample code in the Spotify Web API)
- Spotify Playlist Title (this is the title you want the new playlist to be)

YouTube:
- YouTube Key(this is the key from the YouTube Data API and could be requested by requesting credentials from the GoogleAPI page)
- YouTube Playlist ID (this could be found on the URL of the playlist following 'playlist?list=' )


After cloning this GitHub repo, fill in the information and run the application from the command line and you'll get all the songs from YouTube that Spotify is able to recognize
