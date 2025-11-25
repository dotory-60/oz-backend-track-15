from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema

# 블루프린트 생성
blp = Blueprint(
    "items",                # Blueprint name in Flask
    __name__,                # import_name (__name__)
    url_prefix="/items",    # Blueprint의 기본 URL 경로
    description="Operations on items" # OpenAPI에서 설명하는 글
)

items = []

# ItemList 클래스 - GET 및 POST 요청을 처리
@blp.route("/")
class ItemList(MethodView): # MethodView: HTTP 메서드 기반 처리
    @blp.response(200)
    def get(self):
        return items
    
    @blp.arguments(ItemSchema) # ItemSchema에 맞춰 검증, 역직렬화, 검증 실패는 400 Error
    @blp.response(201, description="Item added") # status code, swagger 문서 설명글
    def post(self, new_data):
        items.append(new_data)
        return new_data
    
# Internal Server Error, 500
@blp.route("/<int:item_id>")
class Item(MethodView):
    @blp.response(200)
    def get(self, item_id):
        item = next((item for item in items if item["id"] == item_id), None)
        if item is None:
            abort(404, message="Item not found")
        return item
    
    @blp.arguments(ItemSchema)
    @blp.response(200, description="Item updated")
    def put(self, new_data, item_id):
        item = next((item for item in items if item["id"] == item_id), None)
        if item is None:
            abort(404, message="Item not found")
        item.update(new_data) # 덮어씀
        return item
    
    @blp.response(204, description="Item deleted")
    def delete(self, item_id):
        global items
        if not any(item for item in items if item["id"] == item_id):
            abort(404, message="Item not found")
        items = [item for item in items if item["id"] != item_id]
        return ''