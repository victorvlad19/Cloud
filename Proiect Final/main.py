import json
import logging
import os
import uuid

from flask import Flask, redirect, render_template, request

from google.cloud import datastore
from google.cloud import storage
from werkzeug.utils import secure_filename

CLOUD_STORAGE_BUCKET = ""
CLOUD_STORAGE_BUCKET_VIDEO = ""
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')


# -------------------------
# PINS
# -------------------------
@app.route('/pins', methods=['GET'])
def  get_pins():
    datastore_client = datastore.Client()
    query = datastore_client.query(kind='Pins')
    pins_entities = list(query.fetch())
    vector = []
    for entity in pins_entities:
        data = {"id": entity.key.name, "lat": entity["lat"], "lng": entity["lng"]}
        vector.append(data)
    return json.dumps(vector)

@app.route('/upload/pins', methods=['POST'])
def upload_pins():
    datastore_client = datastore.Client()
    kind = 'Pins'
    name = str(uuid.uuid4())
    continut = request.json
    cheie = datastore_client.key(kind, name)
    entity = datastore.Entity(cheie)
    entity['lat'] = continut["lat"]
    entity['lng'] = continut["lng"]
    datastore_client.put(entity)
    return str(name)

# -------------------------
# MOVIES
# -------------------------
@app.route('/upload/movies/<pinid>', methods=['POST'])
def upload_movies(pinid):

    # Get file if we have any and UPLOAD to Bucket.
    global filename
    if request.files.get('file', None):
        file = request.files['file']
        filename = secure_filename(file.filename)
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET_VIDEO)
        blob = bucket.blob(file.filename)
        blob.upload_from_string(
            file.read(), content_type=file.content_type)
        blob.make_public()
        file_url = blob.public_url
    else:
        file_url = ""
        filename = ""
    datastore_client = datastore.Client()
    kind = 'Video'
    key = datastore_client.key(kind, filename)
    entity = datastore.Entity(key)
    entity['filename'] = filename
    entity['pinid'] = pinid
    entity['publicurl'] = file_url
    datastore_client.put(entity)
    return redirect('/')

@app.route('/movies/<pinid>', methods=['GET'])
def get_movies(pinid):
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()
    query = datastore_client.query(kind='Video')
    query.add_filter('pinid', '=', pinid)
    messages_entities = list(query.fetch())
    print(messages_entities)
    vector = []
    for entity in messages_entities:
        data = { "filename": entity["filename"], "pinid": entity["pinid"], "publicurl": entity["publicurl"]}
        vector.append(data)
    return json.dumps(vector)

# -------------------------
# COMMENTS
# -------------------------
@app.route('/messages/<pinid>', methods=['GET'])
def  get_messages(pinid):
    datastore_client = datastore.Client()
    query = datastore_client.query(kind='Messages')
    query.add_filter('pinid', '=', pinid)
    messages_entities = list(query.fetch())
    print(messages_entities)
    vector = []
    for entity in messages_entities:
        data = {"id": entity.key.name, "message": entity["message"], "time": entity["time"], "pinid": entity["pinid"],
                "publicurl": entity["publicurl"]}
        vector.append(data)
    return json.dumps(vector)

@app.route('/upload/messages', methods=['POST'])
def upload_messages():
    pinid = request.form['pinid']
    if request.files.get('file', None):
        photo = request.files['file']
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)
        blob = bucket.blob(photo.filename)
        blob.upload_from_string(
            photo.read(), content_type=photo.content_type)
        blob.make_public()
        photo_url = blob.public_url
    else:
        photo_url = ""
    message = request.form['message']
    time = request.form['time']
    datastore_client = datastore.Client()
    kind = 'Messages'
    name = str(uuid.uuid4())
    key = datastore_client.key(kind, name)
    entity = datastore.Entity(key)
    entity['message'] = message
    entity['time'] = time
    entity['pinid'] = pinid
    entity['publicurl'] = photo_url
    datastore_client.put(entity)
    return redirect('/')

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    """.format(e), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9005, debug=True)
