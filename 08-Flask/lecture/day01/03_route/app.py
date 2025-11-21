from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, This is Main Page!"

# Alt + Shift + 화살표(위/아래) : 선택구간이 복사되는 단축키
@app.route("/about")
def about():
    return "This is the about Page!"

# 동적으로 URL 파라미터 값을 받아 처리
@app.route("/user/<username>")
def user_profile(username):
    return f"UserName : {username}"

@app.route("/number/<int:number>")
def unumber(number):
    return f"number : {number}"

# POST 요청하는 법
# (1) postman
# (2) requests
import requests # pip install requests
@app.route("/test")
def test():
    url = "http://127.0.0.1:5000/submit"
    data = "test data"
    response = requests.post(url=url, data=data)

    return Response(response.text, status=response.status_code)


@app.route("/submit", methods=["GET", "POST", "PUT", "DELETE"])
def submit():
    print(request.method)

    if request.method == "GET":
        print("GET method")

    if request.method == "POST":
        print("POST method", request.data)

    return Response("Successfully submitted", status=200)

if __name__ == "__main__":
    app.run(debug=True)