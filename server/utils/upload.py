def upload_files(bucket, files, destinations):
    blobs_uri = dict()
    for (filename, file) in files:
        blob_path = destinations[filename]
        blob = bucket.blob(blob_path)
        blob.upload_from_string(file.read(), content_type=file.content_type)
        blobs_uri[filename] = f"gs://{bucket.name}/{blob_path}"
    return blobs_uri
