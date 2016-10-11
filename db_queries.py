from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'pyDB'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/pyDB'

mongo = PyMongo(app)

@app.route('/staff', methods=['GET'])
def get_all_staff():
    staff = mongo.db.staff
    output = []
    for s in staff.find():
        output.append({'name': s['name'], 'title': s['title'], 'id': s['id']})
    return jsonify({'result': output})

@app.route('/staff_member/<string:name>', methods=['GET'])
def get_staff_member(name):
    staff = mongo.db.staff
    s = staff.find_one({'name': name})
    if s:
        output = {'name': s['name'], 'title': s['title'], 'id': s['id']}
    else:
        output = "No such name"
    return jsonify({'result': output})
# http://localhost:5000/staff_member/Brian <== eg.

@app.route('/staff/<string:title>', methods=['GET'])
def get_staff_by_title(title):
    staff = mongo.db.staff
    output = []
    for s in staff.find({'title': title}):
        output.append({'name': s['name'], 'title': s['title'], 'id': s['id']})
    return jsonify({'result': output})
# http://localhost:5000/staff/QA%20Lead <== Url for blank space

@app.route('/staff_member_id/<string:staff_id>', methods=['GET'])
def get_staff_by_id(staff_id):
    staff = mongo.db.staff
    output = []
    s = staff.find_one({'id': staff_id})
    if s:
        output = {'name': s['name'], 'title': s['title'], 'id': s['id']}
    else:
        output = "ID not found"
    return jsonify({'result': output})
# http://localhost:5000/staff/1 <== eg.

@app.route('/get_original_staff_members', methods=['GET'])
def get_og_staff_members():
    staff = mongo.db.staff
    output = []
    for s in staff.find({'id': {'$lte': '5'}}):
        output.append({'name': s['name'], 'title': s['title'], 'id': s['id']})
    return jsonify({'result': output})
# http://localhost:5000/get_original_staff_members

@app.route('/staff_member/', methods=['POST'])
def add_staff_member():
    staff = mongo.db.staff
    name = request.json['name']
    title = request.json['title']
    member_id = request.json['id']
    staff_id = staff.insert({'name': name, 'title': title, 'id': member_id})
    new_staff_member = staff.find_one({'id': member_id})
    output = {'name': new_staff_member['name'], 'title': new_staff_member['title'], 'id': new_staff_member['id']}
    return jsonify({'result': output})
# request body as JSON -> {"name": "Brian", "id": 1, "title": "QA Test Lead"}

if __name__ == '__main__':
    app.run(debug=True)
