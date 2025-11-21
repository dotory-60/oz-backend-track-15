from flask import Flask
import test

app = Flask(__name__)

host = "127.0.0.1"
port = 8000

# python 실행하면서 app 실행하기
if __name__ == "__main__":
    print("__name__ : ", __name__)
    app.run(debug=True, host=host, port=port)

# 파이썬은 직접 실행한 파일에서는 항상 __name__이 __main__이다.
# 다른 파일에서 import해서 실행될 때는 파일명이 나온다