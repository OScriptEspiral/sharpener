"""
sharpener-admin.

Usage:
  sharpener-admin create_schema
  sharpener-admin populate
  sharpener-admin start_server
"""
from docopt import docopt

import googleclouddebugger
from connectors import exercism
from db import create_schema, database_setup
from dynaconf import settings
from flasgger import Swagger
from google.cloud import storage
from server import create_app

local = __name__ == "__main__"
is_production = settings.ENV == "production"
is_development = not is_production

template = {
    "swagger": "2.0",
    "info": {
        "description": "API for Sharpener",
        "contact": {
            "responsibleDeveloper": "Pedro Morello Abbud",
            "email": "pedro.abbud@usp.br",
        },
        "version": "0.1",
    },
    "securityDefinitions": {
        "cliToken": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
    "host": "sharpener-cloud.appspot" if is_production else "localhost:5000",
    "schemes": ["http", "https"],
}

github_config = {
    "oauth_uri": settings.GITHUB_URI_OAUTH,
    "user_uri": settings.GITHUB_URI_USER,
    "client_id": settings.GITHUB_CLIENT_ID,
    "client_secret": settings.GITHUB_CLIENT_SECRET,
}

if is_production:
    googleclouddebugger.enable()


db_session = database_setup(
    settings.DB_API,
    settings.DB_USERNAME,
    settings.DB_PASSWORD,
    settings.DB_NAME,
    settings.get("DB_CONN_NAME"),
    echo=is_development,
    production=is_production,
)

storage_client = storage.Client()
bucket_submissions = storage_client.bucket(settings.BUCKET_SUBMISSIONS)
bucket_exercises = storage_client.bucket(settings.BUCKET_EXERCISES)
app = create_app(
    db_session,
    github_config,
    settings.FLASK_SECRET,
    bucket_submissions,
    bucket_exercises,
    debug=is_development,
)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["SWAGGER"] = {"title": "Sharpener APIDocs", "uiversion": 3}
swagger = Swagger(app, template=template)

if local:
    args = docopt(__doc__)
    if args["create_schema"]:
        create_schema(
            settings.DB_API,
            settings.DB_USERNAME,
            settings.DB_PASSWORD,
            settings.DB_NAME,
            settings.get("DB_CONN_NAME"),
            echo=is_development,
            production=is_production,
        )

    if args["populate"]:
        exercism.populate_python(
            db_session, storage_client, settings.BUCKET_EXERCISES
        )

        exercism.populate_rust(
            db_session, storage_client, settings.BUCKET_EXERCISES
        )

    if args["start_server"]:
        app.run(debug=local)
