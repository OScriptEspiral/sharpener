from datetime import datetime
from flask import Blueprint, Response
from flask_cors import CORS
import requests
from models import User
from uuid import uuid4

GITHUB_URI_OAUTH = "https://github.com/login/oauth/access_token"
GITHUB_URI_USER = "https://api.github.com/user"
GITHUB_CLIENT_ID = "36689cf871668e2b775e"
GITHUB_CLIENT_SECRET = "0865b1550f1725689b5a2239f5d596d5194b6960"

def fetch_access_token(code):
    params = {
        "code":code,
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
    }
    headers = {
        'Accept': 'application/json'
    }
    github_response = requests.get(GITHUB_URI_OAUTH, params=params,
                                   headers=headers)
    return github_response.json().get('access_token')


def fetch_user_data(access_token):
    headers = {'Authorization': f"token {access_token}"}
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
    }
    github_response = requests.get(GITHUB_URI_USER,
                                   headers=headers,
                                   params=params)

    return github_response.json()


def create_users_blueprint(session, request, default_limit=100):
    users = Blueprint('users', __name__)
    CORS(users)
    @users.route('/', methods=['POST'])
    def new_user():
        data = request.get_json(force=True)
        code = data.get('code')
        if code:
            access_token = fetch_access_token(code)
            print(access_token)
            if access_token:
                user_data = fetch_user_data(access_token)
                new_user = User(
                    email=user_data['email'],
                    name=user_data['name'],
                    nickname=user_data['login'],
                    avatar_url=user_data['avatar_url'],
                    token=uuid4(),
                    github_token=access_token,
                    created_at=datetime.now(),
                )
                session.add(new_user)
                session.commit()

                return Response(status=200)
        return Response(status=400)


    return users

