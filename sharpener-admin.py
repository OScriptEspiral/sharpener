"""
sharpener-admin.

Usage:
  sharpener-admin create_schema
  sharpener-admin populate
  sharpener-admin start_server
"""
import googleclouddebugger
from docopt import docopt
from dynaconf import settings
from google.cloud import storage
from connectors import exercism
from server import create_app
from db import database_setup, create_schema


local = __name__ == "__main__"
is_production = settings.ENV == "production"
is_development = not is_production

github_config = {
    "oauth_uri": settings.GITHUB_URI_OAUTH,
    "user_uri":   settings.GITHUB_URI_USER,
    "client_id":   settings.GITHUB_CLIENT_ID,
    "client_secret": settings.GITHUB_CLIENT_SECRET,
}

if is_production:
    googleclouddebugger.enable()


db_session = database_setup(settings.DB_API,
                            settings.DB_USERNAME,
                            settings.DB_PASSWORD,
                            settings.DB_NAME,
                            settings.get("DB_CONN_NAME"),
                            echo=is_development,
                            production=is_production)

app = create_app(db_session, github_config, settings.FLASK_SECRET,
                 debug=is_development)

if local:
    args = docopt(__doc__)
    if args["create_schema"]:
        create_schema(settings.DB_API,
                      settings.DB_USERNAME,
                      settings.DB_PASSWORD,
                      settings.DB_NAME,
                      settings.get("DB_CONN_NAME"),
                      echo=is_development,
                      production=is_production)

    if args["populate"]:
        storage_client = storage.Client()
        exercism.populate_python(db_session,
                                 storage_client,
                                 settings.BUCKET_EXERCISES)

        exercism.populate_rust(db_session,
                               storage_client,
                               settings.BUCKET_EXERCISES)

    if args["start_server"]:
        app.run(debug=local)
