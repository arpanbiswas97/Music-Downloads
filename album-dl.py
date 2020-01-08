import argparse
import json
import os
from math import log10, ceil
import youtube_dl

# Parse Arguments
parser = argparse.ArgumentParser(description='download the album in albumdata.json')
args = parser.parse_args()

# Load albumdata.json
albumdata = {}
with open('albumdata.json') as albumdata_file:
    albumdata = json.load(albumdata_file)

# Creating Directory if needed
directory = 'downloads/{}/{}/'.format(albumdata['artist'], albumdata['album'])
if not os.path.exists(directory):
    print('Creating Directory', directory)
    os.makedirs(directory)

zpad = ceil(log10(len(albumdata['urls'])+1)) # How much to pad with zeros in track numbers

# Download from YouTube
for i, url in enumerate(albumdata['urls']):
    track_no = str(i+1).zfill(zpad)
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': '{}{} - %(title)s.%(ext)s'.format(directory, track_no),
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0'
        }],
        'postprocessor_args': ['-metadata', 'title='+albumdata['tracks'][i],
                               '-metadata', 'artist='+albumdata['artist'],
                               '-metadata', 'album='+albumdata['album'],
                               '-metadata', 'track='+track_no,
                               '-metadata', 'date='+albumdata['date']]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

print('Done!')
