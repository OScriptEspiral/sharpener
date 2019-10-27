from datetime import datetime
from flask import Blueprint, jsonify, session, Response
import requests
from models import User
from uuid import uuid4


def fetch_access_token(code, github_config):
    params = {
        "code": code,
        "client_id": github_config['client_id'],
        "client_secret": github_config['client_secret'],
    }
    headers = {'Accept': 'application/json'}

    github_response = requests.get(github_config['oauth_uri'], params=params,
                                   headers=headers)
    return github_response.json().get('access_token')


def get_default_oauth_settings(access_token, github_config):
    headers = {'Authorization': f"token {access_token}"}
    params = {
        "client_id": github_config['client_id'],
        "client_secret": github_config['client_secret'],
    }
    return headers, params


def fetch_user_data(access_token, github_config):
    headers, params = get_default_oauth_settings(access_token, github_config)
    github_response = requests.get(github_config['user_uri'],
                                   headers=headers,
                                   params=params)
    fetched_data = github_response.json()
    if not fetched_data.get('email'):
        fetched_data['email'] = fetch_private_email(access_token,
                                                    github_config)

    return fetched_data


def get_primary_email(emails):
    primary_email = [email_metadata['email'] for email_metadata in emails
                     if email_metadata['primary']][0]
    return primary_email


def fetch_private_email(access_token, github_config):
    headers, params = get_default_oauth_settings(access_token, github_config)
    email_resource_uri = f"{github_config['user_uri']}/emails"
    github_response = requests.get(email_resource_uri,
                                   headers=headers,
                                   params=params)
    fetched_data = github_response.json()
    private_email = get_primary_email(fetched_data)
    return private_email


def create_user(db_session, user_data, access_token):
    token = uuid4()
    new_user = User(
        email=user_data.get('email'),
        name=user_data.get('name'),
        nickname=user_data.get('login'),
        avatar_url=user_data.get('avatar_url'),
        github_repositories=user_data.get('repos_url'),
        token=token,
        github_token=access_token,
        created_at=datetime.now(),
    )
    db_session.add(new_user)
    db_session.commit()
    return new_user


def update_user_info(db_session, existing_user, user_data, access_token):
    existing_user.name = user_data.get('name')
    existing_user.nickname = user_data.get('login')
    existing_user.avatar_url = user_data.get('avatar_url')
    existing_user.github_repositories = user_data.get('repos_url')
    existing_user.github_token = access_token
    db_session.commit()


def update_session_info(user):
    session['email'] = user.email
    session['name'] = user.name
    session['token'] = user.token
    session['avatar'] = user.avatar_url
    session['nickname'] = user.nickname


def create_users_blueprint(db_session, request, github_config):
    users = Blueprint('users', __name__)
    @users.route('/<code>', methods=['GET'])
    def authenticate_user(code):
        access_token = fetch_access_token(code, github_config)

        if not access_token:
            return Response(f"Something went wrong. Your github code\
                             was invalid.", status=400)

        user_data = fetch_user_data(access_token, github_config)
        existing_user = db_session.query(User)\
            .filter_by(email=user_data['email'])\
            .first()

        if existing_user:
            update_user_info(db_session, existing_user,
                             user_data, access_token)
            update_session_info(existing_user)
        else:
            new_user = create_user(db_session, user_data, access_token)
            update_session_info(new_user)

        response = {
                "token": session['token'],
                "email": session['email'],
                "name": session['name'],
                "nickname": session['nickname'],
                "avatar": session['avatar'],
            }

        return jsonify(response)
    return users
