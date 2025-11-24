from flask import Flask, abort # API 개발 과정에서 오류를 처리하기 위해 사용

app = Flask(__name__)

@app.route("/example")
def example():
    # 어떠한 조건에서 오류를 발생시키고 처리
    error_condition = True
    if error_condition:
        # abort를 사용할 경우
        abort(500, description="An error occurred while processing the request.")

        # abort가 없는 경우
        # error_response = jsonify({"error": "An error occurred while processing the request."})
        # error_response.status_code = 500
        # return error_response

    # 정상적인 응답
    return "Success!"

if __name__ == "__main__":
    app.run(debug=True)