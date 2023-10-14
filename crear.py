import json
import webbrowser
#import pyautogui
from time import sleep
import time

import argparse
import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
from pprint import pprint
import numpy as np
class month_playlist:
    """ class month playlist

        Parameters:
            - sp - spotipy object
            - song - song object
    """
    def __init__(self, song: object, sp: object):
        self.month = song.month
        self.year = song.year
        self.songs_id = np.array([song.song_id])
        self.playlist_id = ""
    def __str__(self):
        return f"month: {self.month}\n year: {self.year}\n songs_id: {self.songs_id}\n playlist_id: {self.playlist_id}"
    
class song_info:
    """ class song info

        Parameters:
            - day - day added
            - month - month added
            - year - year added
            - songs_id - the songs id
    """
    def __init__(self, track: object):
        self.day = int(track["added_at"][8:10])
        self.month = int(track["added_at"][5:7])
        self.year = int(track["added_at"][:4])
        self.song_id = track["track"]["id"]


    def __str__(self):
        return f"day: {self.day}\n month: {self.month}\n year: {self.year}\n song_id: {self.song_id}\n"


def autenticate(client_id, client_secret, redirect_uri, scope):
    """
        function for spotifyOauth

        Parameters:
            - cliend_id -
            - cliend_secret -
            - redirect_uri -
            - scope - flags
    """
    return SpotifyOAuth(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        scope=scope)


def add_track_to_playlist(sp, track, playlists):
    """
        Function that compare if playlist is already created or not and
        depend of this add or creates a new playlist
    """
    pl_exist = False
    song = song_info(track)
    for playlist in playlists:
        if playlist.year == song.year and playlist.month == song.month:
            playlist.songs_id = np.append(playlist.songs_id, song.song_id)
            pl_exist = True
            break
    if(not pl_exist):

        if(playlists.size != 0):
            print(playlists[-1].songs_id.size)
            n=100
            #split the last playlist
            playlists[-1].songs_id = np.array_split(playlists[-1].songs_id, range(n, len(playlists[-1].songs_id), n))
            #print(playlists[-1].songs_id)
        new_playlist = month_playlist(song, sp)

        playlists= np.append(playlists, new_playlist)
        print("playlist creada") 
    return playlists

def playlist_list_creation():
    scope = 'user-library-read,playlist-modify-public'
    client_id="36b01cc688714a62b1bd951f4e8ace81"
    client_secret="c20b8762c2e6455bba424c1f60e64bf3"
    redirect_uri="http://localhost:1234/"
    sp = spotipy.Spotify(auth_manager=autenticate(client_id,client_secret,redirect_uri,scope))
    user_id = sp.me()['id']

    #playlists que se vayan creeando clase pl_mensual
    playlists = np.empty(0, dtype=object)

    tracks_list = sp.current_user_saved_tracks(limit=50)


    while tracks_list:
        
        #for track in tracks_list["items"]:
        #print(i)
        if tracks_list['next']:
            for track in tracks_list["items"]:
                playlists = add_track_to_playlist(sp, track, playlists)
            tracks_list = sp.next(tracks_list)
        else:
            tracks_list = None
    n=100
    #split the last playlist
    playlists[-1].songs_id = np.array_split(playlists[-1].songs_id, range(n, len(playlists[-1].songs_id), n))

    for playlist in playlists:
        
        playlist.playlist_id = sp.user_playlist_create(sp.me()['id'], f"pl {playlist.month}/{playlist.year}")["id"]
        for songs in playlist.songs_id:
            #song = song_info(playlist.month, playlist.year)
            sp.user_playlist_add_tracks(
                sp.current_user()['id'], playlist.playlist_id, songs
                )
        print(f"playlist {playlist.month}/{playlist.year} created correctly")



def borrar_pl():
    
    # Crea una instancia de la clase SpotifyOAuth para autenticarte en Spotify
    scope = 'user-library-read,playlist-modify-public'
    client_id="36b01cc688714a62b1bd951f4e8ace81"
    client_secret="c20b8762c2e6455bba424c1f60e64bf3"
    redirect_uri="http://localhost:1234/"
    sp = spotipy.Spotify(auth_manager=autenticate(client_id,client_secret,redirect_uri,scope))

    # Obtiene la lista de tus playlists
    playlists = sp.current_user_playlists()

    # Itera sobre las playlists y elimina las que tienen el nombre "pl 9/2023"
    for playlist in playlists['items']:
        if playlist['name'].startswith('pl '):
            sp.user_playlist_unfollow(sp.me()['id'], playlist['id'])
            print(f"Playlist '{playlist['name']}' eliminada.")

    print("Todas las playlists 'pl ' han sido eliminadas.")

def find_july_songs():
    scope = 'user-library-read,playlist-modify-public'
    client_id="36b01cc688714a62b1bd951f4e8ace81"
    client_secret="c20b8762c2e6455bba424c1f60e64bf3"
    redirect_uri="http://localhost:1234/"
    sp = spotipy.Spotify(auth_manager=autenticate(client_id,client_secret,redirect_uri,scope))
    # Obtener la lista de tus playlists
    playlists = sp.current_user_playlists()

    # Buscar la playlist "Junio-Julio 2022"
    target_playlist_name = "Junio-Julio 2022"
    target_playlist_id = None

    for playlist in playlists['items']:
        if playlist['name'] == target_playlist_name:
            target_playlist_id = playlist['id']
            break

    if target_playlist_id is None:
        print(f"No se encontró la playlist '{target_playlist_name}'.")
        return

    # Obtener las canciones de la playlist
    tracks = sp.playlist_tracks(target_playlist_id)

    # Crear una lista para almacenar las canciones de julio
    july_songs = []

    # Buscar las canciones que se estrenaron en julio
    for track in tracks['items']:
        release_date = track['track']['album']['release_date']
        if release_date.startswith("2022-07"):
            july_songs.append(track['track'])

    if july_songs:
        print("Canciones de julio en la playlist:")
        for song in july_songs:
            print(f"'{song['name']}' - Artista: {song['artists'][0]['name']}")

    else:
        print(f"No se encontraron canciones que se estrenaron en julio en la playlist '{target_playlist_name}'.")


def main():
    borrar_pl()
    inicio = time.time()
    #playlist_list_creation()
    print(time.time()-inicio)
    
    #find_july_songs()
    
if __name__ == '__main__':
    main()



    """  track = tracks_list["items"][0]
    tracks_list["items"] = tracks_list["items"][1::]
    pprint(track)
    
    song = song_info(track)
    print(song)
    #primera playlist
    new_playlist = month_playlist(song, sp)
    #print(new_playlist)

    playlists= np.append(playlists, new_playlist)
    #print(playlists[-1])
    """    