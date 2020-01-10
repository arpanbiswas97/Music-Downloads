import argparse
import json
from urllib.parse import urlencode
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from selenium import webdriver

def getSearchString(track_name, artist):
    query = urlencode({'q':'{} {}'.format(track_name, artist)})
    return 'https://music.youtube.com/search?'+query

# Parse Arguments
parser = argparse.ArgumentParser(description='get youtube music links for songs in a spotify album and store them in albumdata.json')
parser.add_argument('link', help='spotify album link')
args = parser.parse_args()

# Spotify Client Credentials
creds = {}
with open('spotify_credentials.json') as creds_file:
    creds = json.load(creds_file)

creds_manager = SpotifyClientCredentials(creds['client_id'], creds['secret'])
sp = spotipy.Spotify(client_credentials_manager=creds_manager)

albumdata = {} # Dictionary to be written as albumdata.json

# Get Album Details
print('Fetching album details.')
album = sp.album(args.link)

print('Artist :', album['artists'][0]['name'])
albumdata['artist'] = album['artists'][0]['name']

print('Album :', album['name'])
albumdata['album'] = album['name']

print('Date :', album['release_date'])
albumdata['date'] = album['release_date']

print('Cover :', album['images'][0]['url'])
albumdata['cover'] = album['images'][0]['url']

# Get Track Names
print('Fetching track names.')
albumdata['tracks'] = []

results = sp.album_tracks(args.link)
tracks = results['items']
while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

for i, track in enumerate(tracks):
    print(i+1, track['name'])
    albumdata['tracks'].append(track['name'])

# Get Track Links
print('Fetching YouTube Music urls.')
albumdata['urls'] = []
driver = webdriver.Firefox(executable_path="webdriver/geckodriver")

for i, track_name in enumerate(albumdata['tracks']):
    print(i+1, track_name, end=' ')
    url = 'empty'
    try:
        # Search in YouTube Music
        driver.get(getSearchString(track_name, albumdata['artist']))
        time.sleep(5)

        # Filter results by songs
        categories_section = driver.find_element_by_id('chips')
        categories = categories_section.find_elements_by_tag_name('ytmusic-chip-cloud-chip-renderer')
        for category in categories:
            if category.find_element_by_tag_name('span').text == 'Songs':
                category.click()
                break
        time.sleep(5)

        # Load the first result
        driver.find_element_by_tag_name('ytmusic-play-button-renderer').click()
        time.sleep(5)

        # Save the url
        url = driver.current_url
    except:
        pass
    print(url)
    albumdata['urls'].append(url)

driver.close()

print('Writing to file.')
with open('albumdata.json', 'w') as albumdata_file:
    albumdata_file.write(json.dumps(albumdata, indent=4))

print('Done!')