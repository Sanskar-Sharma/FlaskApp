from flask_smorest import Blueprint, abort
from flask.views import MethodView

from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel,ItemModel
from schemas import PlainTagSchema, TagSchema,TagAndItemSchema

blp = Blueprint("tags", __name__, description="Operations on Tag")


@blp.route("/tag/<string:tag_id>")
class Tags(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message":"Tag Deleted"}
        abort(404,message = "Item has been linked to this tag, Please Delete the link to continue")






@blp.route("/store/<string:store_id>/tag")
class TagInStore(MethodView):

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["Name"]).first():
            abort(http_status_code=401,messaga ="A tag with that name already exists in that store.")

        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400,message = str(e))

        return tag


@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagstoItem(MethodView):

    @blp.response(200,TagSchema)
    def post(self,item_id,tag_id):

        item = ItemModel.query.get_or_404(item_id)
        tag = ItemModel.query.get_or_404(tag_id)

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message = "An error occurred while inserting the tag.")

        return tag


    def delete(self,item_id,tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = ItemModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message = "An error occurred while deleting the tag.")

        return {"message":"Item removed from tag","item":item,"tag":tag}
