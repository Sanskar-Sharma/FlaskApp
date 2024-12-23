from flask_smorest import Blueprint, abort
from flask.views import MethodView
from db import db
from models import TagModel, StoreModel
from schemas import PlainTagSchema, TagSchema

blp = Blueprint("tags", __name__, description="Operations on Tag")


@blp.route("/tag/<string:tag_id>")
class Tags(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    def delete(self, tag_id):
        pass


@blp.route("/store/<string:store_id>/tag")
class TagInStore(MethodView):

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["Name"]):
            tag = TagModel(**tag_data, store_id=store_id)

