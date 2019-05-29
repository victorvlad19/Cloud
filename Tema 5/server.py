import json
import requests
from bson.json_util import dumps

import pymongo as pymongo
from flask import Flask, render_template, request
from azure.storage.blob import BlockBlobService, PublicAccess
from applicationinsights.flask.ext import AppInsights
from werkzeug.utils import secure_filename
from flask_cors import CORS

account_name = ""
account_key = ""
database = ""
subscription_key = ""

app = Flask(__name__)
CORS(app)
app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = ''
appinsights = AppInsights(app)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return "No File"
        file = request.files['file']
        if file.filename == '':
            return 'No selected file !'
        filename = secure_filename(file.filename)
        # ˅--˅ -- AZURE STORAGE -- ˅--˅
        file_blob = BlockBlobService(account_name=account_name, account_key=account_key)
        container_name = '/'
        file_blob.create_container(container_name)
        file_blob.set_container_acl(container_name, public_access=PublicAccess.Container)
        file_blob.create_blob_from_stream(container_name, filename, file)
        ref = 'https://' + account_name + '.blob.core.windows.net/' + container_name + '/' + filename
        # ˅--˅ -- AZURE DATABASE -- ˅--˅
        db_client = pymongo.MongoClient(database)
        mydb = db_client["video"]
        mycol = mydb["video_col"]
        mydict = {"filename": filename, "url": ref}
        x = mycol.insert_one(mydict)
        # ˅--˅ -- AZURE LOGGER -- ˅--˅
        app.logger.info('A video was uploaded !')
        return "Done"
    except Exception as e:
        print(e)
        return "Fail"

@app.route('/video-list', methods=['GET'])
def video_list():
    # Make database connection
    db_client = pymongo.MongoClient(database)
    db = db_client["video"]
    collection = db['video_col']
    result = []
    for post in collection.find():
        result.append(post)
    # ˅--˅ -- AZURE LOGGER -- ˅--˅
    app.logger.info('Listing all videos...')
    return dumps(result)

@app.route('/similar/<title>', methods=['GET'])
def similar(title):
    # Instantiate the client.
    search_url = ""
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": title, "count": 5, "pricing": "free", "videoLength": "short"}
    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        return json.dumps(search_results)
    except Exception as err:
        print("Fail.. {}".format(err))
        return "Fail"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9005, debug=True)