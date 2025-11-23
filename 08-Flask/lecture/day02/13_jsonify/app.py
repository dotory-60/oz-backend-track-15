from flask import Flask, request, jsonify

app = Flask(__name__)

# 데이터 추가하기
items = []

@app.route('/api/v1/feeds', methods=['GET'])
def show_all_feeds():
	return {'result':'success', 'data': {"feed1":"data", "feed2":"data2"}}

@app.route('/api/v1/feeds/<int:feed_id>', methods=['GET'])
def show_one_feed(feed_id):
    print(feed_id)
    return jsonify({'result':'success', 'data': {"feed1":"data"}})

@app.route('/api/v1/feeds', methods=['POST'])
def create_one_feed():
    name = request.form['name']
    age = request.form['age']
    print(name, age)
    return jsonify({'result':'success'})

@app.route('/create/data', methods=['GET', 'POST'])
def create_data():
    if request.method == "GET":
        return jsonify({"result": items})
    
    if request.method == "POST":
        new_data = request.get_json()
        items.append(new_data)
        return new_data, 201


if __name__ == "__main__":
    app.run(debug=True)