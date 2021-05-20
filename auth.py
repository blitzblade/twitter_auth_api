from flask import Flask, session, request
import os
import json

import tweepy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

current_dir = os.path.dirname(os.path.abspath(__file__))
current_username = os.environ.get('CURRENT_USERNAME')
def get_config(filename,username):
    j = json.load(open(filename))
    return j[username]

@app.route('/')
def home():
    return current_username

@app.route('/api/auth_twitter', methods = ["POST"])
@cross_origin()
def authorize_twitter():

    body = request.get_json()
    print(request.json)
    callback_url = body.get("callback_url")
    print("callback url: ",callback_url)
    print('CURRENT DIRECTORY: ', current_dir)
    config = get_config(f"{current_dir}/config.json",'kwesi_dadson')

    auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"], callback_url)

    try:
        redirect_url = auth.get_authorization_url()
        print("REDIRECT: ", redirect_url)
        return json.dumps({"message":"success", "redirect_url": redirect_url})
    except tweepy.TweepError as ex:
        print(ex)
        print('Error! Failed to get request token.')
        return json.dumps({"message":"Failed to get request token", "redirect_url": None})

@app.route('/api/auth_twitter_callback', methods=["GET"])
@cross_origin()
def twitter_callback():
    try:
        oauth_token = request.args.get('oauth_token')
        oauth_verifier = request.args.get('oauth_verifier')
        authorizer = "kwesi_dadson"
        print("OAUTH TOKEN: ", oauth_token)
        print("OAUTH VERIFIER: ", oauth_verifier)

        config = get_config(f"{current_dir}/config.json",authorizer)
        auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])

        auth.request_token = { "oauth_token": oauth_token, "oauth_token_secret": oauth_verifier }
        auth.get_access_token(oauth_verifier)

        print("ACCESS TOKEN: ",auth.access_token)
        print("ACCESS SECRET: ", auth.access_token_secret)
        api = tweepy.API(auth)

        user = api.me()
        print("API DETAILS: ", user)
        username = user.screen_name
        user_id = user.id
        
        return json.dumps({"message":"success", "user_id": user_id, "username": username, "access_token": auth.access_token, "access_token_secret": auth.access_token_secret})
    except Exception as ex:
        print(ex)
        return json.dumps({"message":"Failed to get tokens"}), 404

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.secret_key = "AUTH_SAM_KWESI_SECRET"
    app.run(port=6000)
