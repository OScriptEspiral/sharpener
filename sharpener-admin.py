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


is_production = settings.ENV == "production"
if is_production:
    googleclouddebugger.enable()

echo = False if is_production else True
db_session = database_setup(settings.DB_API,
                            settings.DB_USERNAME,
                            settings.DB_PASSWORD,
                            settings.DB_NAME,
                            settings.DB_CONN_NAME,
                            echo=echo)

local = __name__ == "__main__"

github_config = {
    "oauth_uri": settings.GITHUB_URI_OAUTH,
    "user_uri":   settings.GITHUB_URI_USER,
    "client_id":   settings.GITHUB_CLIENT_ID,
    "client_secret": settings.GITHUB_CLIENT_SECRET,
}

app = create_app(db_session, github_config, settings.FLASK_SECRET, debug=local)

if local:
    args = docopt(__doc__)
    if args["create_schema"]:
        create_schema(settings.DB_API,
                      settings.DB_USERNAME,
                      settings.DB_PASSWORD,
                      settings.DB_NAME,
                      settings.DB_CONN_NAME,
                      echo=echo)

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
