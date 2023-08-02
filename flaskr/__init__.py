from flask import Flask, jsonify
import os
from flaskr.routes.auth import auth
from flaskr.routes.bookmarks import bookmark
from flaskr.database.database import db
from flask_jwt_extended import JWTManager

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

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
