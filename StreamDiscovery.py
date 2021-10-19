import requests
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

authURL = 'https://id.twitch.tv/oauth2/token'
Client_ID = 'pj5hzast1hte7d3zj7h8qsjuk7kcl4'
Secret  = 't1kccws4tm2qfh6r966hrvphgao3ot'

AutParams = {'client_id': Client_ID,
             'client_secret': Secret,
             'grant_type': 'client_credentials'
             }



AutCall = requests.post(url=authURL, params=AutParams) 
access_token = AutCall.json()['access_token']

head = {
'Client-ID' : Client_ID,
'Authorization' :  "Bearer " + access_token
}


def get_id(name):
    URL_ID = 'https://api.twitch.tv/helix/games?name=' + name
    r = requests.get(URL_ID, headers = head).json()['data']

    return str(r[0]['id'])

def exists(name):
    URL_ID = 'https://api.twitch.tv/helix/games?name=' + name
    r = requests.get(URL_ID, headers = head).json()['data']
    return True if len(r) >= 1 else False
    
def get_streamer_names(name):
    id = get_id(name)
    URL_STREAMS = 'https://api.twitch.tv/helix/streams?language=en&first=99&game_id=' + id
    streams = requests.get(URL_STREAMS, headers = head).json()['data']
    new_streams = []
    count = 0
    for i in range(len(streams)):
        if streams[i]['viewer_count'] < 1000:
            new_streams.append(streams[i])
            count += 1

    for i in range(len(new_streams)):
        id = new_streams[i]['user_id']
        URL = "https://api.twitch.tv/helix/videos?user_id=" + id +"&type=archive&first=100"
        r = requests.get(URL, headers = head).json()['data']
        new_streams[i]['videos'] = int(len(r))
    streams_sorted = sorted(new_streams, key = lambda i: i['videos'], reverse=True)
    return streams_sorted

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if request.form["game"]:
            global game
            game = request.form["game"]
            if exists(game):
                return redirect(url_for("topstreamers"))
    return render_template('index.html')

@app.route("/topstreamers")
def topstreamers():
    streamers = get_streamer_names(game)
    return render_template('streamers.html', len = len(streamers), streamers = streamers)

if __name__ == '__main__':
    app.run(debug=True)