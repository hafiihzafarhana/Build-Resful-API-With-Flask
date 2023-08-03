from flask import Flask, redirect, jsonify
import os
from flaskr.routes.auth import auth
from flaskr.routes.bookmarks import bookmark
from flaskr.database.database import db, Bookmark
from flask_jwt_extended import JWTManager
from flaskr.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR


# berisi kode untuk membuat dan mengonfigurasi objek aplikasi Flask, dan mungkin mendaftarkan blueprint atau modul lain yang relevan dengan aplikasi ini.


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY")
        )

    else:
        app.config.from_mapping(
            test_config
        )
    db.app = app
    db.init_app(app)
    blueprints = [bookmark, auth]

    JWTManager(app)

    for bp in blueprints:
        app.register_blueprint(bp)

    @app.get('/<string:short_url>')
    def redirect_to_url(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()

        if bookmark:
            bookmark.visitor = bookmark.visitor + 1
            db.session.commit()

        return redirect(bookmark.url)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({
            "message": "Request url Not Found"
        }), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({
            "message": "Something went wrong"
        }), HTTP_500_INTERNAL_SERVER_ERROR

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
