from flask import Blueprint, request, jsonify
import validators
from flaskr.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK
from flaskr.database.database import Bookmark, db
from flask_jwt_extended import get_jwt_identity, jwt_required

# auth menajadi nama
# __name__ digunakan untuk mengatur dimana blueprint akan berjalan
bookmark = Blueprint("bookmark", __name__, url_prefix="/api/bookmark")


@bookmark.route("/", methods=['POST', 'GET'])
@jwt_required()
def bookmark_a():
    user_id = get_jwt_identity()
    if request.method == 'POST':
        body = request.get_json().get('body', '')
        url = request.get_json().get('url', '')

        if not validators.url(url):
            return jsonify({
                'message': "Fill with valid url"
            }), HTTP_400_BAD_REQUEST

        if Bookmark.query.filter_by(url=url).first():
            return jsonify({
                'message': "Url already exist"
            }), HTTP_409_CONFLICT

        bookmark = Bookmark(body=body, url=url, user_id=user_id)

        db.session.add(bookmark)
        db.session.commit()

        return jsonify({
            'message': 'Post Bookmark',
            'status': 'CREATED',
            'data': {
                "body": bookmark.body,
                "url": bookmark.url,
                "user_id": bookmark.user_id,
                "short_url": bookmark.short_url,
                "visitor": bookmark.visitor
            }
        }), HTTP_201_CREATED

    if request.method == 'GET':
        bookmarks = Bookmark.query.filter_by(user_id=user_id)

        data = []

        for item in bookmarks:
            data.append({
                "body": item.body,
                "url": item.url,
                "user_id": item.user_id,
                "short_url": item.short_url,
                "visitor": item.visitor
            })

        return jsonify({
            'message': 'Get Bookmarks',
            'status': 'SUCCESS',
            'data': data
        }), HTTP_200_OK
