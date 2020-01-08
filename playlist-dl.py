#!/usr/bin/env python3
import argparse
import os
import subprocess

# Parse Arguments
parser = argparse.ArgumentParser(description="download a playlist from youtube")
parser.add_argument("-d", help="download directory")
parser.add_argument("link", help="youtube playlist link")
args = parser.parse_args()

# Creating Directory if needed
if args.d:
    if not os.path.exists(args.d):
        print("Creating Directory", args.d)
        os.makedirs(args.d)

# Call youtube-dl
if args.d:
    subprocess.call([
        "youtube-dl",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--add-metadata",
        "--output", "%(playlist_index)s - %(title)s.%(ext)s",
        args.link
    ], cwd = args.d)
else:
    subprocess.call([
        "youtube-dl",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--add-metadata",
        "--output", "%(playlist_index)s - %(title)s.%(ext)s",
        args.link
    ])
