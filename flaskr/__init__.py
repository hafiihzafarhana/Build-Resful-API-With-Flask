from flask import Flask, jsonify
import os
from flaskr.routes.auth import auth
from flaskr.routes.bookmarks import bookmark

# berisi kode untuk membuat dan mengonfigurasi objek aplikasi Flask, dan mungkin mendaftarkan blueprint atau modul lain yang relevan dengan aplikasi ini.


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY")
        )

    else:
        app.config.from_mapping(
            test_config
        )

    blueprints = [bookmark, auth]

    for bp in blueprints:
        app.register_blueprint(bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
