import YouTubeMusicClient


'''
INFORMATION TO FILL OUT
'''

#enter spotify information here
user_id = ""
spotify_token = ""
#enter youtube information here
youtube_key = ''

#enter youtube playlist id and the title you want for the new playlist
youtube_playlistId = ""
spotify_playlistTitle = ""


client = YouTubeMusicClient.YouTubeMusic(user_id,spotify_token,youtube_key)
client.playlisttransfer(youtube_playlistId, spotify_playlistTitle)