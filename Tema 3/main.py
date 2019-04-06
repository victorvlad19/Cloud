import json
import logging
import os
import uuid

from flask import Flask, redirect, render_template, request

from google.cloud import datastore
from google.cloud import storage

CLOUD_STORAGE_BUCKET = "cloudweek7"

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')


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

@app.route('/upload/pins', methods=['POST'])
def upload_pins():
    datastore_client = datastore.Client()
    kind = 'Pins'
    name = str(uuid.uuid4())
    content = request.json
    key = datastore_client.key(kind, name)
    entity = datastore.Entity(key)
    entity['lat'] = content["lat"]
    entity['lng'] = content["lng"]
    datastore_client.put(entity)
    return redirect('/')


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


@app.route('/upload/image/<pinid>', methods=['POST'])
def upload_image(pinid):
    photo = request.files['file']
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(photo.filename)
    blob.upload_from_string(
        photo.read(), content_type=photo.content_type)
    blob.make_public()
    return "OK"


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    """.format(e), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
