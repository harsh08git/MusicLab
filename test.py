# import urllib.request
# import re

# search_keyword="VÉRITÉ_Somebody Else"
# search_keyword = search_keyword.replace(' ' ,'_')
# search_keyword = search_keyword.encode('ascii', 'ignore').decode('ascii')
# print(search_keyword)
# html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
# video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
# print("https://www.youtube.com/watch?v=" + video_ids[0])

import pandas as pd

df = pd.read_csv('static/excel/spotify_songs.csv')
print(df[df['track_name'] == 'Armageddon']['playlist_genre'])