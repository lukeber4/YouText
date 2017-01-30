import requests
import json
from bs4 import BeautifulSoup
import re
import sys


def get_transcript_url(video):
    r = requests.get(video)
    soup = BeautifulSoup(r.content, "lxml")
    for i in soup.body.findAll(text=re.compile('TTS_URL'))[0].split('\n'):
        if 'TTS_URL' in i:
            TTS_URL = i.split('"')[1].replace('\\', '').replace('u0026', '&')
            return TTS_URL
    return False


def get_transcript(video):
    url = get_transcript_url(video)
    extra = "&kind&fmt=srv1&lang=en"
    extra2 = "&kind=asr&fmt=srv1&lang=en"
    if url:
        r = requests.get(url+extra)
        if len(r.text) == 0:
            r = requests.get(url+extra2)
        soup2 = BeautifulSoup(r.content, "lxml")
        for line in soup2.text.replace("&#39;", "'").replace('&#39;', "'").replace('&gt;', '>').split("\n"):
            print(line)
    else:
        print('No subtitles available. Sorry.')


def main(video):
    try:
        get_transcript(video)
    except:
        print('Error. Wrong video link perhaps?')


if __name__ == "__main__":
    main(sys.argv[1])
