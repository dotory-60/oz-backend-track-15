from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    data = {
        'title': 'Flask Jinja Template',
        'user': 'jiwon',
        'is_admin': True,
        'items_list': [
            'Item1',
            'Item2',
            'Item3'
        ]
    }
    # (1) rendering html 파일명 입력
    # (2) html로 넘겨줄 데이터 입력
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)