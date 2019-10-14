from dynaconf import settings
from google.cloud import storage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from connectors import exercism


def database_setup(db_uri):
    engine = create_engine(db_uri, echo=True)
    sess = sessionmaker(bind=engine)
    return sess()


session = database_setup(f"{settings.DB_API}{settings.DB_URI}")
storage_client = storage.Client()
exercism.populate_rust(session, storage_client, settings.BUCKET_EXERCISES)
