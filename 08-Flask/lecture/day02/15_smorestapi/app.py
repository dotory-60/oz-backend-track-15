from flask import Flask
from flask_smorest import Api # REST API + 스키마 검증 + OpenAPI 문서화(Swagger UI)
from api import blp

app = Flask(__name__)

# OpenAPI 관련 설정 : REST API를 문서화하고, 테스트하기 쉽게 만들어주는 설정
app.config["API_TITLE"] = "My API"                          # API 문서 제목
app.config["API_VERSION"] = "v1"                            # API 버전 정보
app.config["OPENAPI_VERSION"] = "3.1.3"                     # 사용할 OpenAPI 스펙 버전
app.config["OPENAPI_URL_PREFIX"] = "/"                      # OpenAPI 문서를 노출할 URL prefix
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"       # Swagger UI가 열릴 경로
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"   # Swagger UI 리소스를 불러올 CDN


api = Api(app)
api.register_blueprint(blp)

if __name__ == "__main__":
    app.run(debug=True)