import argparse
import os
import youtube_dl

# Parse Arguments
parser = argparse.ArgumentParser(description='download a song from youtube')
parser.add_argument('-d', help='download directory')
parser.add_argument('link', help='youtube song link')
args = parser.parse_args()

# Creating Directory if needed
directory = 'downloads/'
if args.d:
    directory += args.d
if not os.path.exists(directory):
    print('Creating Directory', directory)
    os.makedirs(directory)

# Use youtube_dl
ydl_opts = {
    'format': 'bestaudio',
    'outtmpl': directory+'%(title)s.%(ext)s',
    'noplaylist': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '0'
    }, {
        'key': 'FFmpegMetadata'
    }]
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([args.link])

print('Done!')
