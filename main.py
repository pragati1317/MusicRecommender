import pickle
from typing import Any, List

import pandas as pd
import numpy as np

from flask import Flask, request, render_template
from pandas import DataFrame, Series
from PIL import Image

PopularMusic = pd.read_pickle('popularSong.pkl')
songs = pd.read_pickle('songs.pkl')
train: DataFrame | Any = pd.read_pickle('train.pkl')

img: list[str] = [
    'https://static3.depositphotos.com/1008070/243/i/600/depositphotos_2439271-stock-photo-beautiful-singer.jpg',
    'https://st2.depositphotos.com/1284069/6896/i/950/depositphotos_68969355-stock-photo-beautiful-african-woman-singing-with.jpg',
    'https://st4.depositphotos.com/20363444/41444/i/600/depositphotos_414440548-stock-photo-kyiv-ukraine-august-2020-angry.jpg',
    'https://st.depositphotos.com/11625992/52155/i/600/depositphotos_521550384-stock-photo-beautiful-hispanic-woman-singing-stage.jpg',
    'https://static6.depositphotos.com/1003368/638/i/450/depositphotos_6389159-stock-photo-sexy-woman-with-cowboy-hat.jpg',
    'https://st.depositphotos.com/1001959/4405/i/600/depositphotos_44057103-stock-photo-rock-singer.jpg',
    'https://c4.wallpaperflare.com/wallpaper/708/292/852/actress-taylor-swift-wallpaper-preview.jpg',
     'https://c4.wallpaperflare.com/wallpaper/63/216/922/adele-beautiful-women-s-white-and-black-long-sleeve-shirt-wallpaper-preview.jpg',
    'https://c4.wallpaperflare.com/wallpaper/244/950/570/hollywood-celebrities-female-celebrities-wallpaper-preview.jpg',
    'https://c4.wallpaperflare.com/wallpaper/148/975/645/katy-perry-singer-katy-perry-wallpaper-preview.jpg',
    'https://c4.wallpaperflare.com/wallpaper/567/185/199/cute-girl-avril-lavigne-avril-lavigne-wallpaper-preview.jpg',
    'https://c4.wallpaperflare.com/wallpaper/779/228/36/cumming-on-the-old-avril-lavigne-maxim-pic-wallpaper-preview.jpg'

]
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def most_frequent(list):
    return max(set(list), key=list.count)


## Function for Popular Music

def MyPopularSong(user: object) -> object:
    """

    :rtype: object
    """
    col = train.columns
    global UserData
    UserData = pd.DataFrame(columns=col)
    UserDetails = (np.where(train['msno'] == user))[0]
    # UserData=UserData.append((train.iloc[UserDetails]), ignore_index=True)
    for i in range(len(UserDetails)):
        temp = (train.iloc[UserDetails[i]])

        UserData = UserData._append(temp, ignore_index=True)
        ##end of For loop

    ## Lets work for song data  , By extracting the song_id and then language
    LanguageData = []
    MySong = pd.DataFrame(columns=songs.columns)

    for i in range(len(UserData)):
        SongId = (UserData.iloc[i])['song_id']
        d = (songs['song_id'] == SongId)
        d = d[d].index

        ## end of For Loop
        if d.empty:
            continue
        # print(d)
        lan = (songs.iloc[d])
        value = lan['language'].to_string(index=False)
        LanguageData.append(value)

    # lan.count('52.0')
    Newlan = []
    for i in range(len(LanguageData)):
        if (LanguageData[i]):
            Newlan.append(float(LanguageData[i]))

    mx = most_frequent(Newlan)
    print(mx)

    return mx


def PopularRecommend(mx):
    global UserPopularSong
    UserPopularSong = pd.DataFrame(columns=songs.columns)
    x = (PopularMusic['language'] == mx)
    x = x[x].index
    print(x[4])
    for i in range(len(x)):
        d = PopularMusic.iloc[x[i]]
        UserPopularSong = UserPopularSong._append(d, ignore_index=True)

#
# us = "Xumu+NIjS6QYVxDS4/t3SawvJ7viT9hPKXmf0RtLNx8="
us = 'FGtllVqz18RPiwJj/edr2gV78zirAiY/9SmYvia+kCg='
cnt = MyPopularSong(us)
PopularRecommend(cnt)
#
pickle.dump(UserPopularSong, open('UserPopularSong.pkl', 'wb'))
UserPopularSong = pd.read_pickle('UserPopularSong.pkl')

app = Flask(__name__, template_folder='template')


@app.route('/')
def index():
    # img = Image.open('Music1.jpg')
    return render_template('index.html',
                           image=list(img),
                           Popular_Artist=list(UserPopularSong['artist_name'].values),
                           Popular_Composer=list(UserPopularSong['composer'].values),
                           YourLanguage=list(UserPopularSong['language'].values)
                           )


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
if __name__ == '__main__':
    print_hi('PyCharm')
    app.run(debug=True)
