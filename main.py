# shows artist info for a URN or URL
import json
import webbrowser
import pyautogui
from time import sleep

import argparse
import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import pprint
def credentialsSP():
    client_id = "36b01cc688714a62b1bd951f4e8ace81"
    client_secret = "c20b8762c2e6455bba424c1f60e64bf3"
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="",
                                                   client_secret="",
                                                   redirect_uri="http://localhost:1234/",
                                                   scope="playlist-modify-public"))
    #return spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))
"""    SPOTIFY_CLIENT_ID = "36b01cc688714a62b1bd951f4e8ace81"
    SPOTIFY_SECRET = "c20b8762c2e6455bba424c1f60e64bf3"
    REDIRECT_URL = "http://example.com"

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri=REDIRECT_URL,
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_SECRET,
            cache_path="token.txt"
        )
    )"""

def search():
    #client_id = "36b01cc688714a62b1bd951f4e8ace81"
    #client_secret = "c20b8762c2e6455bba424c1f60e64bf3"
    #if len(sys.argv) > 1:
    #    search_str = sys.argv[1]
    #else:
    search_str = 'Radiohead'

    #sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id,client_secret))
    sp = credentialsSP()

    result = sp.search(search_str)

    print(result)
    print(result['tracks']['items'][0]['name'])
    pass
def playlistTrack():

    sp = credentialsSP()

    pl_id = 'spotify:playlist:1jcK5NN5HrIFTtb9OR42Mv'
    #pl_id = 'spotify:playlist:37i9dQZF1EJzFhm9q1BSY5'
    cancion = 'spotify:track:1jcK5NN5HrIFTtb9OR42Mv'
    offset = 0

    while True:
        response = sp.playlist_items(pl_id,
                                     offset=offset,
                                     fields='items.track.id,total',
                                     additional_types=['track'])

        if len(response['items']) == 0:
            break

        print(response['items'])
        print(response['items'][0]['track']['id'])
        offset = offset + len(response['items'])
        print(offset, "/", response['total'])
        cancion = f"spotify:track:{response['items'][0]['track']['id']}"
        #webbrowser.open(cancion)
        webbrowser.open("spotify:playlist:37i9dQZF1EJzFhm9q1BSY5")
        sleep(5)
        #pyautogui.hotkey("alt","tab")
        for it in range(2):
            pyautogui.press('tab')
            print(it)



        pyautogui.press("enter")

    pass
def nombresCancionesPlaylist():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="36b01cc688714a62b1bd951f4e8ace81",
                                                   client_secret="c20b8762c2e6455bba424c1f60e64bf3",
                                                   redirect_uri="http://localhost:1234/",
                                                   scope="playlist-read-private"))

    playlist_id = 'spotify:user:spotifycharts:playlist:2XmS7Z1Zkx08KvhMaJ5TWx'
    results = sp.playlist(playlist_id)
    i = 1
    for track in results["tracks"]["items"]:
        if track["track"] != None:
            print(i," ",track["track"]["name"])
            i+=1
    pass





def getArgsAñadirPlaylist():
    parser = argparse.ArgumentParser(description='Adds track to user playlist')
    parser.add_argument('-t', '--tids', action='append',
                        required=True, help='Track ids')
    parser.add_argument('-p', '--playlist', required=True,
                        help='Playlist to add track to')
    return parser.parse_args()


def añadirAPlaylist():
    """logger = logging.getLogger('examples.add_tracks_to_playlist')
    logging.basicConfig(level='DEBUG')
    scope = 'playlist-modify-public'"""

    args = getArgsAñadirPlaylist()

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="36b01cc688714a62b1bd951f4e8ace81",
                                                   client_secret="c20b8762c2e6455bba424c1f60e64bf3",
                                                   redirect_uri="http://localhost:1234/",
                                                   scope="playlist-modify-public"))
    sp.playlist_add_items(args.playlist, args.tids)



def getArgsCancionGuardada():
    parser = argparse.ArgumentParser(description='Add tracks to Your '
                                     'Collection of saved tracks')
    parser.add_argument('-t', '--tids', action='append',
                        required=True, help='Track ids')
    return parser.parse_args()


def añadirCancionGuardada():
    scope = 'user-library-modify'

    logger = logging.getLogger('examples.add_a_saved_track')
    logging.basicConfig(level='DEBUG')
    args = getArgsCancionGuardada()
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="36b01cc688714a62b1bd951f4e8ace81",
                                                   client_secret="c20b8762c2e6455bba424c1f60e64bf3",
                                                   redirect_uri="http://localhost:1234/",
                                                   scope="user-library-modify"))

    sp.current_user_saved_tracks_add(tracks=args.tids)




def show_tracks(results):
    for item in results['items']:
        track = item['track']
        print("%32.32s %s" % (track['artists'][0]['name'], track['name']))

def mostrarCancionesGuardadas():
    scope = 'user-library-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="36b01cc688714a62b1bd951f4e8ace81",
                                                   client_secret="c20b8762c2e6455bba424c1f60e64bf3",
                                                   redirect_uri="http://localhost:1234/",
                                                   scope=scope))
    results = sp.current_user_saved_tracks()
    show_tracks(results)

    while results['next']:
        #print(results)
        results = sp.next(results)
        show_tracks(results)
def añadirCancionAPl(lista, results, i):
    for item in results['items']:
        track = item['track']
        print("%i %32.32s %s %s" % (i, track['artists'][0]['name'], track['name'], item['added_at'][0:10]))
        lista.append(track['id'])
        i+=1



def crearPlMensual():
    scope = 'user-library-read,playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="36b01cc688714a62b1bd951f4e8ace81",
                                                   client_secret="c20b8762c2e6455bba424c1f60e64bf3",
                                                   redirect_uri="http://localhost:1234/",
                                                   scope=scope))


    user_id = sp.me()['id']
    newPlaylist = sp.user_playlist_create(user_id, "playlist prueba")
    newPlaylist = newPlaylist['id']
    print(newPlaylist)
    lista = []
    i = 1
    results = sp.current_user_saved_tracks()
    añadirCancionAPl(lista, results, i)
    i+=20
    #print(lista)
    sp.playlist_add_items(newPlaylist, lista)
    while results['next']:
        lista = []
        #print(results)
        results = sp.next(results)
        añadirCancionAPl(lista, results, i)
        #print(lista)
        i += 20
        sp.playlist_add_items(newPlaylist, lista)

def player():

    #scope = "user-read-playback-state,user-modify-playback-state,user-top-read"
    scope = "user-read-playback-state,user-modify-playback-state"
    sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(client_id="36b01cc688714a62b1bd951f4e8ace81",
                                                   client_secret="c20b8762c2e6455bba424c1f60e64bf3",
                                                   redirect_uri="http://localhost:1234/",
                                                   scope=scope))
    # Shows playing devices
    res = sp.devices()
    print(res)
    sp.shuffle(state=True)
    # Change track
    sp.start_playback(context_uri= "spotify:playlist:2XmS7Z1Zkx08KvhMaJ5TWx", position_ms=5)

    # Change volume
    sp.volume(100)
    """sleep(2)
    sp.volume(50)
    sleep(2)
    sp.volume(100)"""
    topTracks = sp.current_user_top_tracks()
    #print(topTracks)
def manipularString():
    playlistsNames = ["January", "February", "March",
                      "April", "May", "June",
                      "July","August", "September",
                      "October", "November", "December"]
    scope = 'playlist-read-private'
    sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(client_id="36b01cc688714a62b1bd951f4e8ace81",
                                                                 client_secret="c20b8762c2e6455bba424c1f60e64bf3",
                                                                 redirect_uri="http://localhost:1234/",
                                                                 scope=scope))


    results = sp.current_user_playlists(limit=50)
    i=0
    for i, item in enumerate(results['items'], start=i):
        print("%d %s" % (i, item['name']))
    while results['next']:
        for i, item in enumerate(results['items'],start=i):
            print("%d %s" % (i, item['name']))
        results = sp.next(results)
    print(playlistsNames[11])
    for i in playlistsNames:
        print(i)
    pass
def main():
    manipularString()
    #crearPlMensual()
    #player()
    #mostrarCancionesGuardadas()
    #añadirCancionGuardada()
    #añadirAPlaylist()
    #nombresCancionesPlaylist()
    #playlistTrack()
    #search()

if __name__ == '__main__':
    main()
