# Name: downloadPlaylistMp3FromYoutube.py
# Version: 1.6
# Author: pantuts vs arh
# Email: pantuts@gmail.com
# Description: Parse URLs in Youtube User's Playlist and download in mp3 format multithreading
# Use python3 and later
# Agreement: You can use, modify, or redistribute this tool under
# the terms of GNU General Public License (GPLv3).
# This tool is for educational purposes only. Any damage you make will not affect the author.
# Usage: python3 youParse.py youtubeURLhere maxVideosToPorcessAtTheSameTime
# Example: python downloadPlaylistMp3FromYoutube.py 'https://www.youtube.com/watch?v=Ey_hgKCCYU4&list=RDQMsGiVnMp7oYc' 10
# Comment: dont forget cover the link through quotes due python cut link if find an ampersand
 
import re
import urllib.request
import urllib.error
import sys
import time
import os
import subprocess
from threading import Thread, Lock

def downloadMp3(urlSong):
    subprocess.call(["youtube-dl","-cit","-x","--audio-format","mp3",urlSong])

def runThreads(threads):
    for x in threads:
        x.start()
    for x in threads:
        x.join()
    threads.clear()

 
def crawl(url,maxThreadsAtTheTime):
    sTUBE = ''
    cPL = ''
    amp = 0
    final_url = []
    
    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]
            
    else:
        print('Incorrect Playlist.')
        exit(1)
    
    try:
        yTUBE = urllib.request.urlopen(url).read()
        sTUBE = str(yTUBE)
    except urllib.error.URLError as e:
        print(e.reason)
    
    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, sTUBE)
 
    if mat:
          
        for PL in mat:
            yPL = str(PL)
            if '&' in yPL:
                yPL_amp = yPL.index('&')
            final_url.append('http://www.youtube.com/' + yPL[:yPL_amp])
 
        all_url = list(set(final_url))
 
        i = 0
        p = 0
        threads = []
        while i < len(all_url):
            sys.stdout.write(all_url[i] + '\n')
            urlSong = all_url[i] + '\n'
            threads.append(Thread(target=downloadMp3,args=(urlSong, ) ))
            if (p>maxThreadsAtTheTime) or ((len(all_url)-i) == p): #Taking until max or the remaining
                runThreads(threads)
                p = 0
            time.sleep(0.04)
            i = i + 1
            p = p + 1
        print("Done!")
        
        
    else:
        print('No videos found.')
        exit(1)
        
if len(sys.argv) < 3 or len(sys.argv) > 3:
    print('USAGE: python youtubeListToMp3Parallel.py \'youtubePlayList\' maxVideosAtTheTime')
    print('Example: python youtubeListToMp3Parallel.py \'https://www.youtube.com/watch?v=KWGrPNqz4uc&list=PLRZlMhcYkA2GDuq-8BTLzTRGpwNsGlWjj\' 10')
    exit(1)
    
else:
    url = sys.argv[1]
    maxThreadsAtTheTime = int(sys.argv[2])
    if 'http' not in url:
        url = 'http://' + url
    crawl(url,maxThreadsAtTheTime)
