import os
import subprocess
import re

from pytube import *

def dnld(l, filepath):
        # converts the link to a YouTube object
        yt = YouTube(l)
        # takes first stream; since ffmpeg will convert to mp3 anyway
        music = yt.streams.first()
        # gets the filename of the first audio stream
        default_filename = music.default_filename
        print("Downloading " + default_filename + "...")
        # downloads first audio stream
        music.download()
        # creates mp3 filename for downloaded file
        new_filename = default_filename[0:-3] + "mp3"
        # converts mp4 audio to mp3 audio
        subprocess.run(['ffmpeg', '-i', 
            os.path.join(filepath, default_filename),
            os.path.join(filepath, new_filename)
        ])
        os.remove(default_filename)
    

def run(pl,filepath):
    os.chdir(filepath)

    pl._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    links = pl.video_urls
    print("Downloading {} songs".format(len(links)))
    
    brokenLinks = []
    for l in links:
        try:
            dnld(l, filepath)
        except:
            print("\n{} broke, trying again".format(l))
            try:
                dnld(l, filepath)
                print("Got it...\n")
            except:
                print("Still failed...\n")
                brokenLinks.append(l)
    
    print("Download finished.")
    print(brokenLinks)

if __name__ == "__main__":

    filepath = "D:\\Music\\"
    url = "https://www.youtube.com/playlist?list=PLl5jedZJvdnihKRAXRAlZA0y3frsY77Ms"
    pl = Playlist(url)
    run(pl)
