from flask import Blueprint, request, jsonify
import validators
from flaskr.constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK
from flaskr.database.database import Bookmark, db
from flask_jwt_extended import get_jwt_identity, jwt_required

# auth menajadi nama
# __name__ digunakan untuk mengatur dimana blueprint akan berjalan
bookmark = Blueprint("bookmark", __name__, url_prefix="/api/bookmark")


@bookmark.route("/<int:bookmark_id>", methods=['PUT', 'GET', "DELETE"])
@jwt_required()
def bookmark_do_a(bookmark_id):
    user_id = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(
        user_id=user_id, id=bookmark_id).first()

    if not bookmark:
        return jsonify({
            'message': f"Bookmark not found or can't access by user with id {user_id}"
        }), HTTP_404_NOT_FOUND

    if request.method == 'PUT':
        body = request.get_json().get('body', '')
        url = request.get_json().get('url', '')

        if not validators.url(url):
            return jsonify({
                'message': "Fill with valid url"
            }), HTTP_400_BAD_REQUEST

        bookmark.url = url
        bookmark.body = body

        db.session.commit()

        return jsonify({
            'message': f'Update bookmark by id {bookmark.id}',
            'status': 'SUCCESS',
            'data': {
                "body": bookmark.body,
                "url": bookmark.url,
                "user_id": bookmark.user_id,
                "short_url": bookmark.short_url,
                "visitor": bookmark.visitor
            }
        }), HTTP_200_OK

    if request.method == 'GET':
        return jsonify({
            'message': f'Get bookmark by id {bookmark.id}',
            'status': 'SUCCESS',
            'data': {
                "body": bookmark.body,
                "url": bookmark.url,
                "user_id": bookmark.user_id,
                "short_url": bookmark.short_url,
                "visitor": bookmark.visitor
            }
        }), HTTP_200_OK

    if request.method == 'DELETE':
        db.session.delete(bookmark)
        db.session.commit()

        return jsonify({
            'message': f'Delete bookmark by id {bookmark.id}',
            'status': 'SUCCESS',
        }), HTTP_200_OK
    return


@bookmark.route("/", methods=['POST', 'GET'])
@jwt_required()
def bookmark_do_b():
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
        # Give pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        bookmarks = Bookmark.query.filter_by(
            user_id=user_id).paginate(page=page, per_page=per_page)

        data = []

        for item in bookmarks:
            data.append({
                "body": item.body,
                "url": item.url,
                "user_id": item.user_id,
                "short_url": item.short_url,
                "visitor": item.visitor
            })

        meta_data = {
            "page": bookmarks.page,
            "count_pages": bookmarks.pages,
            "total_datas": bookmarks.total,
            "prev_page": bookmarks.prev_num,
            "next_page": bookmarks.next_num,
            "has_next": bookmarks.has_next,
            "has_prev": bookmarks.has_prev
        }

        return jsonify({
            'message': 'Get bookmarks',
            'status': 'SUCCESS',
            'data': {"bookmark_data": data, "pagination_data": meta_data}
        }), HTTP_200_OK
