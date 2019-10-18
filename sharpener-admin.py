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
from api import create_app
from db import database_setup, create_schema


is_production = settings.ENV == "production"
if is_production:
    googleclouddebugger.enable()

echo = False if is_production else True
session = database_setup(settings.DB_API,
                         settings.DB_USERNAME,
                         settings.DB_PASSWORD,
                         settings.DB_NAME,
                         settings.DB_CONN_NAME,
                         echo=echo)

app = create_app(session)

if __name__ == "__main__":
    args = docopt(__doc__)
    if args["create_schema"]:
        create_schema(settings.DB_API, settings.DB_URI)

    if args["populate"]:
        storage_client = storage.Client()
        exercism.populate_python(session,
                                 storage_client,
                                 settings.BUCKET_EXERCISES)

        exercism.populate_rust(session,
                               storage_client,
                               settings.BUCKET_EXERCISES)

    if args["start_server"]:
        app.run()
