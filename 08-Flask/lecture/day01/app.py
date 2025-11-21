from flask import Flask

app = Flask(__name__)

# flask server 실행 방법
# python app.py 또는 flask run

# 주의사항
# WARNING: This is a development server. 
# Do not use it in a production deployment. Use a production WSGI server instead.

# 지금 실행 중인 서버는 개발 서버입니다. 운영 환경에서는 WSGI 서버를 사용하세요.
# 개발 서버는 (자동 재시작, 디버그 표시, 보안성 낮음, 속도 느림) 특징을 갖기 때문입니다.