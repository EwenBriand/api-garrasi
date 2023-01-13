from flask import Flask, request, send_file, render_template
from flask_cors import CORS
import sys
import asyncio
from pprint import pprint
import json
from waitress import serve
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

client = MongoClient(
    'mongodb+srv://Garry:MgA2kGlMI2PNkR90@cluster0.jbale6t.mongodb.net/test')
site = client['garrasi']['site']
user = client['garrasi']['user']
msg = client['garrasi']['msg']

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# @app.route('/sc_neo', methods=['GET'])
# def sc_neo():
#     data = request.args.get('url')
#     if data is not None:
#         res = back.scrap_neo_ft(data)
#         if res == None:
#             return 'Error func return None', 400
#         return res, 200
#     else:
#         return 'Bad request', 400

# @app.route('/marque_neo', methods=['POST'])
# def marque_neo():
#     data = None
#     content_type = request.headers.get('Content-Type')
#     if (content_type == 'application/json'):
#         data = request.get_json()

#     if data is not None:
#         res = back.marque(back.get_head())
#         if res == None:
#             return 'Error func return None', 400
#         return res, 200
#     else:
#         return 'Bad request', 400


@app.route('/add_site', methods=['POST'])
def add_site():
    data = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()

    if data is not None:
        if site.find_one({"url": data["url"]}) == None:
            new_s = {"url": data["url"], "QnA": [],
                     "feedback": [], "discuchat": []}
            res = site.update_one({"url": new_s["url"]}, {
                "$set": new_s}, upsert=True)
            return new_s, 200
        else:
            return 'Bad url', 400
    else:
        return 'Bad request', 400


@app.route('/add_msg', methods=['POST'])
def add_msg():
    data = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()

    if data is not None:
        id = ObjectId()
        print(data)
        new_msg = {"_id": id,
                   "channel": data["channel"],
                   "username": data["username"],
                   "color": data["color"],
                   "content": data["content"],
                   "upvote": [],
                   "downvote": [],
                   "date": datetime.now().strftime("%d/%m/%Y"),
                   "time": datetime.now().strftime("%H:%M"),
                   "response": []
                   }
        msg.insert_one(new_msg)
        site.update_one({"url": data["url"]}, {"$push": {data["channel"]: id}})
        return 'Msg added', 200
    else:
        return 'Bad request', 400


@app.route('/add_response', methods=['POST'])
def add_response():
    data = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()

    if data is not None:
        id = ObjectId()
        print(data)
        new_msg = {"_id": id,
                   "channel": data["channel"],
                   "username": data["username"],
                   "color": data["color"],
                   "content": data["content"],
                   "upvote": [],
                   "downvote": [],
                   "date": datetime.now().strftime("%d/%m/%Y"),
                   "time": datetime.now().strftime("/%H:/%M"),
                   "response": []
                   }
        msg.insert_one(new_msg)
        msg.update_one({"_id": ObjectId(data["id"])}, {
                       "$push": {"response": id}})
        return 'Msg added', 200
    else:
        return 'Bad request', 400


@app.route('/get_ch', methods=['POST'])
def get_ch():
    data = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()

    if data is not None:
        all_ms = site.find_one({"url": data["url"]})[data["channel"]]
        print(all_ms)
        all_data = list(msg.find({"_id": {"$in": all_ms}}))
        for i in all_data:
            i["_id"] = str(i["_id"])
            for j in range(len(i['response'])):
                i['response'][j] = str(i['response'][j])
        pprint(all_data)
        return all_data, 200
    return 'Bad request', 400


@app.route('/get_response', methods=['POST'])
def get_res():
    data = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()

    if data is not None:
        all_ms = msg.find_one({"_id": ObjectId(data["id"])})['response']
        print(all_ms)
        all_data = list(msg.find({"_id": {"$in": all_ms}}))
        for i in all_data:
            i["_id"] = str(i["_id"])
            for j in range(len(i['response'])):
                i['response'][j] = str(i['response'][j])
        pprint(all_data)
        return all_data, 200
    return 'Bad request', 400


@app.route('/upvote', methods=['POST'])
def upvote():
    data = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()

    if data is not None:
        ms = msg.find_one({"_id": ObjectId(data["id"])})
        if ms["username"] != data["username"] and data["username"] not in ms['upvote']:
            msg.update_one({"_id": ObjectId(data["id"])}, {
                "$push": {'upvote': data["username"]},
                "$pull": {'downvote': data["username"]}
            })
            return 'Up vote', 200
    return 'Bad Request', 400


@app.route('/downvote', methods=['POST'])
def downvote():
    data = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()

    if data is not None:
        ms = msg.find_one({"_id": ObjectId(data["id"])})
        if ms["username"] != data["username"] and data["username"] not in ms['downvote']:
            msg.update_one({"_id": ObjectId(data["id"])}, {
                "$pull": {'upvote': data["username"]},
                "$push": {'downvote': data["username"]}
            })
            return 'Down vote', 200
    return 'Bad Request', 400

# @app.route('/test', methods=['POST'])
# def test():
#     data = None
#     content_type = request.headers.get('Content-Type')
#     if (content_type == 'application/json'):
#         data = request.get_json()

#     if data is not None:
#         print("find")
#         print(msg.update_one({"_id": ObjectId(data["id"])}, {
#             "$push": {"response": "id"}}))

    # return "OK", 200


if __name__ == '__main__':
    # serve(app, host='0.0.0.0', port=8080)
    app.run(debug=True)

#  http://127.0.0.1:5000
