from flask import Blueprint

# auth menajadi nama
# __name__ digunakan untuk mengatur dimana blueprint akan berjalan
bookmark = Blueprint("bookmark", __name__, url_prefix="/api/bookmark")


@bookmark.get("/")
def get_all():
    return []


@bookmark.get("/<id>")
def get_by_id(id=None):
    return []
