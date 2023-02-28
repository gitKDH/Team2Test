from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
import datetime as dt

from pymongo import MongoClient
client = MongoClient('localhost',27017)
db = client.dbjungle


@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['GET'])
def read_memos():
    result = list(db.memos.find({}, {'_id': 0}).sort('like', -1))
    return jsonify({'result': 'success', 'memos': result})

@app.route('/memo', methods=['POST'])

def post_memo():
    x = dt.datetime.now()
    id = (x.strftime('%c').replace(" " , "").replace(":",""))
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    memo = {'title': title_receive, 'content': content_receive, 'like' : 0, 'id' : id}
    db.memos.insert_one(memo)
    return jsonify({'result': 'success'})

@app.route('/api/like', methods=['POST'])
def like_memo():
    id_receive = request.form['id_give']
    memo = db.memos.find_one({'id': id_receive})
    new_like = memo['like']+1
    db.memos.update_one({'id':id_receive},{'$set':{'like':new_like}})
    return jsonify({'result': 'success'})

@app.route('/api/delete', methods=['POST'])
def delete_memo():
    id_receive = request.form['id_give']
    db.memos.delete_one({'id': id_receive})
    return jsonify({'result': 'success'})

@app.route('/api/change', methods=['POST'])
def save_memo():
    id_receive = request.form['id_give']
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    db.memos.update_one({'id':id_receive},{'$set':{'title' : title_receive}})
    db.memos.update_one({'id':id_receive},{'$set':{'content': content_receive}})
    return jsonify({'result': 'success'})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)